from dataclasses import dataclass
from typing import Iterable
from .gate_evaluator import evaluate, PromotionDecision
@dataclass(frozen=True)
class PromotionResult:
 repository:str; commit_sha:str; decision:PromotionDecision; reason:str
def evaluate_matrix(repository:str,commit_sha:str,required_gates:Iterable,expected_branch:str=None)->PromotionResult:
 gates=list(required_gates)
 if expected_branch is not None:
  for g in gates:
   actual=getattr(g,'branch',None)
   if actual is not None and actual!=expected_branch: return PromotionResult(repository,commit_sha,PromotionDecision.BLOCK,'wrong branch')
 d=evaluate(gates)
 return PromotionResult(repository,commit_sha,d,'all required gates SUCCESS' if d==PromotionDecision.ALLOW else 'one or more required gates unresolved or failed')
