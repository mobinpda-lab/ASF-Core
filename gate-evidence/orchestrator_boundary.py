from gate_evidence.evaluator.gate_matrix import evaluate_matrix

def promotion_decision(repository, commit_sha, evidence_matrix):
    """Production Orchestrator integration boundary; fail-closed on supplied matrix."""
    return evaluate_matrix(repository, commit_sha, evidence_matrix)
