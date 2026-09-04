"""Evidence observation and gate integration primitives."""
from .ci_observer import EvidenceObserver, EvidenceRecord, Visibility
from .gate_integration import PromotionGate, promotion_matrix
from .provider import EvidenceProvider, ObservationState, ProviderObservation, uncertainty_blocks
from .github_adapter import GitHubAdapter

__all__ = ["EvidenceObserver", "EvidenceRecord", "Visibility", "PromotionGate", "promotion_matrix", "EvidenceProvider", "ObservationState", "ProviderObservation", "uncertainty_blocks", "GitHubAdapter"]
