from typing import Dict, Tuple
from nexus_c2.core.models import TokenBudget


class TokenBudgetManager:
    """Silnik kontroli kosztów i deterministycznego przycinania kontekstu agentów."""

    def __init__(self) -> None:
        self.agent_budgets: Dict[str, TokenBudget] = {}

    def register_agent(self, agent_id: str, budget: TokenBudget) -> None:
        """Rejestruje profil budżetowy dla danego agenta."""
        self.agent_budgets[agent_id] = budget

    def authorize_execution(
        self, agent_id: str, estimated_tokens: int, estimated_cost: float
    ) -> Tuple[bool, str]:
        """Weryfikuje, czy agent ma wystarczające środki/tokeny na przetworzenie zadania."""
        budget = self.agent_budgets.get(agent_id)
        if not budget:
            return False, f"Agent {agent_id} nie jest zarejestrowany w systemie budżetowym."

        if not budget.can_process(estimated_tokens, estimated_cost):
            return (
                False,
                f"Przekroczono limit budżetu dla {agent_id}! "
                f"Wymagane: {estimated_tokens} tokenów / ${estimated_cost:.4f}, "
                f"Dostępne: {budget.max_token_limit - budget.current_context_tokens} tokenów / ${budget.max_cost_usd - budget.accumulated_cost_usd:.4f}",
            )

        # Aktualizacja stanu po zatwierdzeniu
        budget.current_context_tokens += estimated_tokens
        budget.accumulated_cost_usd += estimated_cost
        return True, "Zadanie zatwierdzone do realizacji."

    def compress_context_history(self, context_text: str, target_reduction: float = 0.3) -> str:
        """
        Symuluje kompresję kontekstu / prompt caching poprzez odrzucenie zbędnych bajtów
        i zachowanie kluczowych struktur danych.
        """
        lines = context_text.strip().split("\n")
        retained_count = max(1, int(len(lines) * (1.0 - target_reduction)))
        compressed = lines[:retained_count]
        compressed.append(f"... [Context compressed by {target_reduction * 100:.0f}% to fit budget constraints]")
        return "\n".join(compressed)