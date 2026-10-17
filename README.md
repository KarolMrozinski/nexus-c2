# ⚡ NEXUS-C2: Zero-Trust Multi-Agent C2 Architecture

[![Architecture](https://img.shields.io/badge/architecture-Zero--Trust%20%7C%20Envelope%20Encryption-blue)](#)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](#)
[![License](https://img.shields.io/badge/license-Non--Commercial-orange)](#)

> **NEXUS-C2** to zdecentralizowana platforma orkiestracji autonomicznych agentów wykorzystująca zasady **Zero-Trust**, kryptograficzne szyfrowanie wiadomości (**Envelope Encryption / AES-256-GCM**) oraz silnik **Deterministycznego Budżetowania Tokenów/Kontekstu**.

---

## ✨ Kluczowe Funkcjonalności

- **Zero-Trust Envelope Encryption:** Bezpieczne pakowanie ładunku wiadomości w szyfrowane koperty z unikalnym kluczem roboczym (DEK/KEK Pattern, `cryptography`).
- **Deterministic Token & Cost Budgeting:** Rygorystyczna weryfikacja kosztów finansowych oraz limitów tokenów przed przekazaniem egzekucji do agenta LLM.
- **Multi-Agent DAG Flow Orchestration:** Sekwencyjne dispatchowanie zadań między rolami (Orchestrator, Worker, Auditor) w oparciu o autoryzowane przydziały.
- **Rich Interactive CLI:** Konsolowy interfejs raportujący stan szyfrowania, budżetów oraz wyników orkiestracji (`Rich` + `Typer`).

---

## 🏗️ Architektura Przepływu Zadań

```mermaid
graph TD
    classDef crypto fill:#4a5568,stroke:#cbd5e0,stroke-width:1px,color:#fff;
    classDef agent fill:#2b6cb0,stroke:#90cdf4,stroke-width:2px,color:#fff;

    Orchestrator["ORCHESTRATOR_MAIN"]
    AnalysisWorker["WORKER_ANALYSIS"]
    BudgetManager["TokenBudgetManager"]

    Orchestrator -->|1. Request Authorization| BudgetManager
    BudgetManager -->|2. Approved / Rejected| Orchestrator
    Orchestrator -->|3. Encrypted Envelope AES-256-GCM| AnalysisWorker
    AnalysisWorker -->|4. Decrypt and Execute Payload| AnalysisWorker

    class BudgetManager crypto;
    class Orchestrator,AnalysisWorker agent;
```