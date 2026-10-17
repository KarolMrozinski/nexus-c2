import typer
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON

from nexus_c2.core.models import TokenBudget
from nexus_c2.crypto.envelope import EnvelopeCryptoEngine

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


if __name__ == "__main__":
    app()