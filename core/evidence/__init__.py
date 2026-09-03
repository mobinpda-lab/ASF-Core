"""Evidence observation and gate integration primitives."""
from .ci_observer import EvidenceObserver, EvidenceRecord, Visibility
from .gate_integration import PromotionGate, promotion_matrix

__all__ = ["EvidenceObserver", "EvidenceRecord", "Visibility", "PromotionGate", "promotion_matrix"]
