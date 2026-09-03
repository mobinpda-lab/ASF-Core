from typing import Dict,List
from gate_evidence.collector.models import GateEvidence
class EvidenceStore:
 def __init__(self): self._records:Dict[str,GateEvidence]={}
 def append(self,evidence_id:str,record:GateEvidence)->None:
  if evidence_id in self._records: raise ValueError('duplicate evidence_id')
  self._records[evidence_id]=record
 def get(self,evidence_id:str)->GateEvidence:return self._records[evidence_id]
 def all(self)->List[GateEvidence]:return list(self._records.values())
