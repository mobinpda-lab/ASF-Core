'use strict';

const fs = require('fs');
const { routedResponse } = require('./provider_router');

function firstBalancedJsonObject(text) {
  const source = String(text || '');
  const start = source.indexOf('{');
  if (start < 0) return '';
  let depth = 0;
  let inString = false;
  let escaped = false;
  for (let index = start; index < source.length; index++) {
    const char = source[index];
    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (char === '\\') {
        escaped = true;
      } else if (char === '"') {
        inString = false;
      }
      continue;
    }
    if (char === '"') {
      inString = true;
      continue;
    }
    if (char === '{') depth += 1;
    if (char === '}') {
      depth -= 1;
      if (depth === 0) return source.slice(start, index + 1);
    }
  }
  return '';
}

function parseJson(text) {
  const cleaned = String(text || '').trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '');
  try {
    return JSON.parse(cleaned);
  } catch (firstError) {
    const extracted = firstBalancedJsonObject(cleaned);
    if (!extracted) throw firstError;
    return JSON.parse(extracted);
  }
}

function extractExactScope(body, availablePaths) {
  const text = String(body || '');
  if (!text.includes('NIRA_SELF_COMPLETION_TASK: true')) return availablePaths;
  const section = text.split('## Exact autonomous scope', 2)[1] || '';
  const untilNext = section.split(/\n##\s+/, 1)[0];
  const requested = untilNext
    .split('\n')
    .map(line => line.match(/^\s*-\s+(.+?)\s*$/)?.[1] || '')
    .filter(Boolean);
  if (!requested.length) return availablePaths;
  const allowed = new Set(requested);
  return availablePaths.filter(path => allowed.has(path));
}

function countOccurrences(haystack, needle) {
  if (!needle) return 0;
  let count = 0;
  let offset = 0;
  while (offset <= haystack.length) {
    const index = haystack.indexOf(needle, offset);
    if (index < 0) break;
    count += 1;
    offset = index + Math.max(needle.length, 1);
  }
  return count;
}

function simulateEdits(edits, files) {
  const original = new Map(files.map(file => [file.path, file.content]));
  const working = new Map(original);
  for (let index = 0; index < edits.length; index++) {
    const edit = edits[index];
    const current = working.get(edit.path);
    if (typeof current !== 'string') {
      return { problem: `edit ${index + 1} targets unknown path`, working, original };
    }
    const occurrences = countOccurrences(current, edit.old);
    if (occurrences !== 1) {
      return {
        problem: `edit ${index + 1} old substring must match exactly once; observed=${occurrences}`,
        working,
        original
      };
    }
    const updated = current.replace(edit.old, edit.new);
    if (updated.length > 180000) {
      return { problem: `edit ${index + 1} makes file exceed bounded size`, working, original };
    }
    working.set(edit.path, updated);
  }
  return { problem: '', working, original };
}

async function run({ github, context, core }) {
  const env = process.env;
  const [owner, repo] = String(env.CLIENT_REPOSITORY || '').split('/');
  if (!owner || !repo) throw new Error('INVALID_CLIENT_REPOSITORY');
  if (!/^\d+$/.test(String(env.FENCE_TOKEN || '')) || Number(env.FENCE_TOKEN) <= 0) {
    throw new Error('INVALID_FENCE_TOKEN');
  }

  const mainRef = await github.rest.git.getRef({ owner, repo, ref: 'heads/main' });
  const observed = mainRef.data.object.sha;
  if (observed !== env.EXPECTED_MAIN_SHA) {
    core.setFailed(`NIRA_FENCING=HEAD_DRIFT expected=${env.EXPECTED_MAIN_SHA} observed=${observed}`);
    return;
  }

  const issue = await github.rest.issues.get({ owner, repo, issue_number: Number(env.ISSUE_NUMBER) });
  const tree = await github.rest.git.getTree({ owner, repo, tree_sha: observed, recursive: 'true' });
  const allPaths = tree.data.tree
    .filter(item => item.type === 'blob' && item.path && !item.path.startsWith('.git/'))
    .map(item => item.path)
    .slice(0, 2500);
  const paths = extractExactScope(issue.data.body, allPaths);
  if (!paths.length) throw new Error('NIRA_BLOCKED=NO_ALLOWED_SOURCE_PATHS');

  async function requestValidatedJson(messages, validate, label, maxOutputTokens) {
    let request = [...messages];
    for (let attempt = 1; attempt <= 2; attempt++) {
      const result = await routedResponse(request, {
        env,
        core,
        maxOutputTokens,
        expectJson: true
      });
      const raw = result.output_text;
      try {
        const parsed = parseJson(raw);
        const problem = validate(parsed);
        if (problem) throw new Error(problem);
        core.notice(`NIRA_MODEL_OUTPUT=${label}_VALID attempt=${attempt} provider=${result.provider}`);
        return parsed;
      } catch (error) {
        const reason = String(error.message || error).slice(0, 1000);
        if (attempt >= 2) {
          throw new Error(`NIRA_${label}_OUTPUT_INVALID_AFTER_REPAIR: ${reason}`);
        }
        core.warning(`NIRA_MODEL_OUTPUT=${label}_REPAIR attempt=${attempt} reason=${reason}`);
        request = [
          ...messages,
          {
            role: 'user',
            content: [{
              type: 'input_text',
              text: 'Your previous response was rejected by NIRA local validation. Reason: ' +
                reason +
                '. Return corrected JSON only. Do not broaden scope. Previous response excerpt:\n' +
                String(raw).slice(0, 6000)
            }]
          }
        ];
      }
    }
    throw new Error(`NIRA_${label}_REPAIR_EXHAUSTED`);
  }

  const selectionMessages = [
    {
      role: 'system',
      content: [{
        type: 'input_text',
        text: 'You are a bounded software-factory planner. Select only the smallest relevant source/test/documentation files needed to fix the supplied GitHub issue. Never select secrets, .git paths, GitHub workflow files, generated binaries, lockfiles, or unrelated files. Return JSON only: {"paths":["..."]}. Maximum 8 paths.'
      }]
    },
    {
      role: 'user',
      content: [{
        type: 'input_text',
        text: `Repository: ${env.CLIENT_REPOSITORY}\nIssue #${env.ISSUE_NUMBER}: ${issue.data.title}\n${issue.data.body || ''}\n\nAvailable files:\n${paths.join('\n')}`
      }]
    }
  ];
  const selection = await requestValidatedJson(
    selectionMessages,
    value => {
      if (!Array.isArray(value?.paths) || value.paths.length === 0 || value.paths.length > 8) {
        return 'selection paths must contain 1..8 entries';
      }
      for (const path of value.paths) {
        if (typeof path !== 'string' || !paths.includes(path)) return 'selection contains unknown or out-of-scope path';
        if (path.startsWith('.github/') || path.includes('..') || /(^|\/)\.env($|\.)/i.test(path) || /secret|credential|token/i.test(path)) {
          return 'selection contains forbidden path';
        }
      }
      return '';
    },
    'SELECTION',
    2000
  );

  const files = [];
  for (const path of selection.paths) {
    const current = await github.rest.repos.getContent({ owner, repo, path, ref: observed });
    if (Array.isArray(current.data) || current.data.type !== 'file') throw new Error(`NIRA_NOT_FILE=${path}`);
    const content = Buffer.from(current.data.content, 'base64').toString('utf8');
    if (content.length > 120000) throw new Error(`NIRA_FILE_TOO_LARGE=${path}`);
    files.push({ path, sha: current.data.sha, content });
  }

  const editMessages = [
    {
      role: 'system',
      content: [{
        type: 'input_text',
        text: 'You are the NIRA bounded code worker. Fix only the supplied issue using the supplied files. Preserve architecture and existing patterns. Do not invent dependencies. Do not change secrets, workflows, CI policy, permissions, release controls, or unrelated behavior. Return JSON only: {"summary":"...","edits":[{"path":"exact existing path","old":"exact existing UTF-8 substring that occurs once","new":"replacement UTF-8 substring"}]}. Use the smallest edits possible, maximum 16 edits across maximum 8 files. The old substring must be copied exactly from supplied content and uniquely identify the edit location. If the issue cannot be safely fixed from the supplied context, return {"summary":"BLOCKED: ...","edits":[]}. Never return markdown fences.'
      }]
    },
    {
      role: 'user',
      content: [{
        type: 'input_text',
        text: `Repository: ${env.CLIENT_REPOSITORY}\nIssue #${env.ISSUE_NUMBER}: ${issue.data.title}\n${issue.data.body || ''}\n\nExact leased main SHA: ${observed}\n\nFiles:\n${files.map(file => `--- ${file.path} (sha ${file.sha}) ---\n${file.content}`).join('\n')}`
      }]
    }
  ];
  const editResult = await requestValidatedJson(
    editMessages,
    value => {
      if (!Array.isArray(value?.edits) || value.edits.length > 16) {
        return 'edits must contain 0..16 replacements';
      }
      if (value.edits.length === 0 && !String(value?.summary || '').startsWith('BLOCKED:')) {
        return 'zero edits requires a BLOCKED summary';
      }
      const distinctPaths = new Set();
      let totalChars = 0;
      for (const edit of value.edits) {
        if (!edit || typeof edit.path !== 'string' || typeof edit.old !== 'string' || typeof edit.new !== 'string') {
          return 'each edit requires path, old, and new UTF-8 strings';
        }
        if (!edit.old || edit.old === edit.new) return 'each edit must replace a non-empty old substring with different content';
        if (!files.some(file => file.path === edit.path)) return 'edit is outside selected context';
        if (edit.path.startsWith('.github/') || edit.path.includes('..') || /(^|\/)\.env($|\.)/i.test(edit.path) || /secret|credential|token/i.test(edit.path)) {
          return 'edit contains forbidden path';
        }
        distinctPaths.add(edit.path);
        totalChars += edit.old.length + edit.new.length;
      }
      if (distinctPaths.size > 8) return 'edits exceed changed-file bound';
      if (totalChars > 120000) return 'replacement payload exceeds bounded size';
      return simulateEdits(value.edits, files).problem;
    },
    'PATCH',
    6000
  );

  if (editResult.edits.length === 0) {
    throw new Error(`NIRA_WORKER_BLOCKED_SAFE: ${String(editResult.summary || '').slice(0, 1000)}`);
  }

  const simulation = simulateEdits(editResult.edits, files);
  if (simulation.problem) throw new Error(`NIRA_EDIT_SIMULATION_INVALID: ${simulation.problem}`);
  const replacements = files
    .map(file => ({
      path: file.path,
      sha: file.sha,
      original: file.content,
      content: simulation.working.get(file.path)
    }))
    .filter(file => file.content !== file.original);
  if (!replacements.length || replacements.length > 8) throw new Error('NIRA_EDIT_RESULT_CHANGED_FILE_BOUND');

  const suffix = `${env.ISSUE_NUMBER}-${env.WORKER_ID}`.replace(/[^A-Za-z0-9._-]/g, '-').slice(0, 80);
  const branch = `nira/worker-${suffix}`;
  try {
    await github.rest.git.getRef({ owner, repo, ref: `heads/${branch}` });
    throw new Error('DUPLICATE_EXECUTION_BRANCH');
  } catch (error) {
    if (error.status !== 404) throw error;
  }
  await github.rest.git.createRef({ owner, repo, ref: `refs/heads/${branch}`, sha: observed });

  const changed = [];
  for (const replacement of replacements) {
    const updated = await github.rest.repos.createOrUpdateFileContents({
      owner,
      repo,
      path: replacement.path,
      message: `fix(nira): bounded worker change for issue #${env.ISSUE_NUMBER}`,
      content: Buffer.from(replacement.content, 'utf8').toString('base64'),
      branch,
      sha: replacement.sha,
      committer: { name: 'NIRA Factory Worker', email: 'nira-factory@users.noreply.github.com' },
      author: { name: 'NIRA Factory Worker', email: 'nira-factory@users.noreply.github.com' }
    });
    changed.push({ path: replacement.path, commit: updated.data.commit.sha });
  }

  const pr = await github.rest.pulls.create({
    owner,
    repo,
    title: `fix(nira): bounded worker execution #${env.ISSUE_NUMBER}`,
    head: branch,
    base: 'main',
    draft: true,
    maintainer_can_modify: false,
    body: [
      '## NIRA bounded real code execution',
      '',
      `- NIRA worker: ${env.WORKER_ID}`,
      `- Lease: ${env.LEASE_ID}`,
      `- Fence: ${env.FENCE_TOKEN}`,
      `- Exact leased main SHA: ${observed}`,
      `- Issue: #${env.ISSUE_NUMBER}`,
      `- Provider order: ${process.env.NIRA_PROVIDER_ORDER || 'gemini,openrouter,openai'}`,
      `- Edit operations: ${editResult.edits.length}`,
      `- Changed files: ${changed.map(item => item.path).join(', ')}`,
      '',
      'Worker has no merge/promotion authority. Client CI/security/release gates remain authoritative.'
    ].join('\n')
  });

  fs.writeFileSync('nira-worker-evidence.txt', [
    'NIRA_EXECUTION=REAL_CODE_WORKER',
    `NIRA_CLIENT_REPOSITORY=${env.CLIENT_REPOSITORY}`,
    `NIRA_ISSUE=${env.ISSUE_NUMBER}`,
    `NIRA_EXPECTED_MAIN_SHA=${observed}`,
    `NIRA_WORKER_ID=${env.WORKER_ID}`,
    `NIRA_LEASE_ID=${env.LEASE_ID}`,
    `NIRA_FENCE_TOKEN=${env.FENCE_TOKEN}`,
    `NIRA_BRANCH=${branch}`,
    `NIRA_PR=${pr.data.number}`,
    `NIRA_EDIT_OPERATIONS=${editResult.edits.length}`,
    `NIRA_CHANGED_FILES=${changed.map(item => item.path).join(',')}`,
    `NIRA_WORKER_SUMMARY=${String(editResult.summary || '').replace(/\n/g, ' ')}`
  ].join('\n') + '\n');

  core.setOutput('branch', branch);
  core.setOutput('commit_sha', pr.data.head.sha);
  core.setOutput('pr_number', pr.data.number);
  core.notice(`NIRA_BRANCH=${branch}`);
  core.notice(`NIRA_COMMIT=${pr.data.head.sha}`);
  core.notice(`NIRA_PR=${pr.data.number}`);
}

module.exports = {
  countOccurrences,
  extractExactScope,
  firstBalancedJsonObject,
  parseJson,
  simulateEdits,
  run
};
