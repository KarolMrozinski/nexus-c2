from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    ORCHESTRATOR = "ORCHESTRATOR"
    ANALYSIS_WORKER = "ANALYSIS_WORKER"
    EXECUTION_WORKER = "EXECUTION_WORKER"
    AUDITOR = "AUDITOR"


class EnvelopeHeader(BaseModel):
    """Nagłówek koperty kryptograficznej Zero-Trust."""
    message_id: str
    sender_id: str
    recipient_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    algorithm: str = "AES-GCM-256"
    key_fingerprint: str


class EncryptedEnvelope(BaseModel):
    """Kryptograficznie zabezpieczona koperta przesyłana między agentami."""
    header: EnvelopeHeader
    encrypted_dek: str  # Encrypted Data Encryption Key (Base64)
    nonce: str          # Initialization Vector / Nonce (Base64)
    ciphertext: str     # Szyfrowany ładunek / komenda (Base64)
    tag: str            # Authentication Tag (Base64)


class TokenBudget(BaseModel):
    """Silnik deterministycznego budżetowania kontekstu/tokenów dla LLM."""
    max_token_limit: int = Field(default=4096, ge=512)
    current_context_tokens: int = Field(default=0, ge=0)
    max_cost_usd: float = Field(default=0.10, ge=0.0)
    accumulated_cost_usd: float = Field(default=0.0, ge=0.0)

    def can_process(self, estimated_tokens: int, estimated_cost: float) -> bool:
        """Sprawdza, czy zapytanie mieści się w dopuszczalnym budżecie."""
        within_tokens = (self.current_context_tokens + estimated_tokens) <= self.max_token_limit
        within_cost = (self.accumulated_cost_usd + estimated_cost) <= self.max_cost_usd
        return within_tokens and within_cost