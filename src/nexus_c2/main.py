import typer
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON

from nexus_c2.core.models import TokenBudget
from nexus_c2.crypto.envelope import EnvelopeCryptoEngine
from nexus_c2.core.budget import TokenBudgetManager
from nexus_c2.core.models import TokenBudget
from nexus_c2.core.orchestrator import MultiAgentOrchestrator
from nexus_c2.core.models import AgentRole, TokenBudget

app = typer.Typer(help="NEXUS-C2: Zero-Trust Multi-Agent C2 Architecture")
console = Console()


@app.command(name="encrypt-test")
def test_crypto() -> None:
    """Testuje szyfrowanie kopertowe i weryfikację Zero-Trust między agentami."""
    console.print(
        Panel.fit(
            "[bold cyan]⚡ NEXUS-C2 Zero-Trust Cryptography Engine[/bold cyan]\n[dim]Testing Envelope Encryption (AES-256-GCM / DEK-KEK Pattern)[/dim]",
            border_style="cyan",
        )
    )

    crypto = EnvelopeCryptoEngine()
    payload = {
        "command": "EXECUTE_RECONNAISSANCE",
        "target_subnet": "10.0.4.0/24",
        "priority": "HIGH",
        "restricted": True,
    }

    with console.status("[bold green]Szyfrowanie ładunku i tworzenie koperty Zero-Trust..."):
        envelope = crypto.encrypt_payload(
            message_id="MSG-99201",
            sender_id="AGENT_ORCHESTRATOR",
            recipient_id="AGENT_WORKER_ALPHA",
            payload=payload,
        )

    console.print("\n[bold yellow]🔒 Wygenerowana Szyfrowana Koperta (Zero-Trust Envelope):[/bold yellow]")
    console.print_json(envelope.model_dump_json())

    with console.status("[bold green]Odszyfrowywanie i weryfikacja autentyczności..."):
        decrypted_payload = crypto.decrypt_envelope(envelope)

    console.print("\n[bold green]✔ Odszyfrowany Ładunek (Verifiable Payload):[/bold green]")
    console.print_json(data=decrypted_payload)

@app.command(name="budget-check")
def test_budget() -> None:
    """Testuje silnik deterministycznego budżetowania tokenów i kosztów dla agentów."""
    console.print(
        Panel.fit(
            "[bold cyan]⚡ NEXUS-C2 Deterministic Token Budgeting[/bold cyan]\n[dim]Context & Cost Limit Enforcement Engine[/dim]",
            border_style="cyan",
        )
    )

    manager = TokenBudgetManager()
    
    # Rejestracja agenta z rygorystycznym budżetem ($0.05 / max 2048 tokenów)
    manager.register_agent("AGENT_WORKER_ALPHA", TokenBudget(max_token_limit=2048, max_cost_usd=0.05))

    # Test 1: Pierwsze zapytanie mieści się w limicie
    ok1, msg1 = manager.authorize_execution("AGENT_WORKER_ALPHA", estimated_tokens=1024, estimated_cost=0.02)
    console.print(f"Task 1 (1024 tokens, $0.02): [{'green' if ok1 else 'red'}]{msg1}[/{'green' if ok1 else 'red'}]")

    # Test 2: Drugie zapytanie przekracza budżet finansowy
    ok2, msg2 = manager.authorize_execution("AGENT_WORKER_ALPHA", estimated_tokens=1500, estimated_cost=0.04)
    console.print(f"Task 2 (1500 tokens, $0.04): [{'green' if ok2 else 'red'}]{msg2}[/{'green' if ok2 else 'red'}]")

@app.command(name="run-flow")
def run_orchestration_flow() -> None:
    """Uruchamia sekwencję orkiestracji przepływu zadań między agentami Zero-Trust."""
    console.print(
        Panel.fit(
            "[bold cyan]⚡ NEXUS-C2 Multi-Agent Orchestration Flow[/bold cyan]\n[dim]DAG Task Dispatch with Zero-Trust & Budget Enforcement[/dim]",
            border_style="cyan",
        )
    )

    orchestrator = MultiAgentOrchestrator()

    # Rejestracja agentów
    orchestrator.register_agent(
        "ORCHESTRATOR_MAIN",
        AgentRole.ORCHESTRATOR,
        TokenBudget(max_token_limit=8192, max_cost_usd=1.0),
    )
    orchestrator.register_agent(
        "WORKER_ANALYSIS",
        AgentRole.ANALYSIS_WORKER,
        TokenBudget(max_token_limit=4096, max_cost_usd=0.20),
    )

    task = {
        "action": "THREAT_INTELLIGENCE_SCAN",
        "target": "c5isr-internal-network",
        "depth": "FULL_AUDIT",
    }

    with console.status("[bold green]Orkiestrowanie zadania i szyfrowanie Zero-Trust..."):
        result = orchestrator.dispatch_task(
            sender_id="ORCHESTRATOR_MAIN",
            recipient_id="WORKER_ANALYSIS",
            task_payload=task,
            estimated_tokens=512,
            estimated_cost=0.01,
        )

    console.print("\n[bold green]✔ Wynik Orkiestracji Przepływu Zadań:[/bold green]")
    console.print_json(data=result)

if __name__ == "__main__":
    app()