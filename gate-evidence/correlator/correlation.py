from dataclasses import dataclass
from typing import Iterable, List
from gate_evidence.collector.models import GateEvidence
@dataclass(frozen=True)
class CorrelationKey:
 repository:str; commit_sha:str; workflow:str=''; event:str=''; run_id:int=0; job_id:int=0; artifact_id:int=0; check_id:int=0
def correlate(evidence:Iterable[GateEvidence],repository:str,commit_sha:str)->List[GateEvidence]:
 return [x for x in evidence if x.repository==repository and x.commit_sha==commit_sha]
def branch_matches(actual_branch:str, expected_branch:str)->bool:
 return actual_branch==expected_branch
