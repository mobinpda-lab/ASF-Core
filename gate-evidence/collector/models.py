from dataclasses import dataclass
from enum import Enum
from typing import Optional
class EvidenceStatus(str,Enum):
 SUCCESS='SUCCESS'; FAILURE='FAILURE'; PENDING='PENDING'; NOT_FOUND='NOT_FOUND'; NOT_EXPOSED='NOT_EXPOSED'
@dataclass(frozen=True)
class GateEvidence:
 repository:str; commit_sha:str; workflow:Optional[str]=None; run_id:Optional[int]=None; job:Optional[str]=None; job_id:Optional[int]=None; artifact:Optional[str]=None; artifact_id:Optional[int]=None; check:Optional[str]=None; check_id:Optional[int]=None; event:Optional[str]=None; branch:Optional[str]=None; status:EvidenceStatus=EvidenceStatus.NOT_FOUND; timestamp:str=''
class WorkflowRunCollector:
 def collect(self,repository,commit_sha): raise NotImplementedError
class CheckRunCollector:
 def collect(self,repository,commit_sha): raise NotImplementedError
class JobResultCollector:
 def collect(self,repository,run_id): raise NotImplementedError
class ArtifactResultCollector:
 def collect(self,repository,run_id): raise NotImplementedError
