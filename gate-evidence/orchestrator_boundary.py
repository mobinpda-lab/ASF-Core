from gate_evidence.evaluator.gate_matrix import evaluate_matrix
def promotion_decision(repository,commit_sha,evidence_matrix,expected_branch=None):
 return evaluate_matrix(repository,commit_sha,evidence_matrix,expected_branch)
