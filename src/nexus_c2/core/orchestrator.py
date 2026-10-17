from typing import List, Dict, Any
from nexus_c2.core.models import TokenBudget, AgentRole
from nexus_c2.core.budget import TokenBudgetManager
from nexus_c2.crypto.envelope import EnvelopeCryptoEngine


class MultiAgentOrchestrator:
    """Silnik orkiestracji agentów egzekwujący budżet oraz szyfrowanie Zero-Trust."""

    def __init__(self) -> None:
        self.crypto = EnvelopeCryptoEngine()
        self.budget_manager = TokenBudgetManager()
        self.registered_agents: Dict[str, AgentRole] = {}

    def register_agent(self, agent_id: str, role: AgentRole, budget: TokenBudget) -> None:
        """Rejestruje agenta wraz z jego rolą i profilem budżetowym."""
        self.registered_agents[agent_id] = role
        self.budget_manager.register_agent(agent_id, budget)

    def dispatch_task(
        self,
        sender_id: str,
        recipient_id: str,
        task_payload: Dict[str, Any],
        estimated_tokens: int,
        estimated_cost: float,
    ) -> Dict[str, Any]:
        """
        Orkiestruje wysłanie zadania: weryfikuje budżet, szyfruje wiadomość do koperty Zero-Trust,
        a następnie deszyfruje ją po stronie odbiorcy.
        """
        # 1. Walidacja budżetu tokenowego
        authorized, reason = self.budget_manager.authorize_execution(
            recipient_id, estimated_tokens, estimated_cost
        )
        if not authorized:
            return {"status": "REJECTED", "reason": reason}

        # 2. Szyfrowanie ładunku (Envelope Encryption)
        envelope = self.crypto.encrypt_payload(
            message_id="TASK-EVT-01",
            sender_id=sender_id,
            recipient_id=recipient_id,
            payload=task_payload,
        )

        # 3. Odszyfrowanie przez agenta docelowego
        decrypted_payload = self.crypto.decrypt_envelope(envelope)

        return {
            "status": "EXECUTED",
            "message_id": envelope.header.message_id,
            "recipient": recipient_id,
            "decrypted_payload": decrypted_payload,
        }