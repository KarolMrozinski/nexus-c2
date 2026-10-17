# ⚡ NEXUS-C2: Zero-Trust Multi-Agent C2 Architecture

[![Architecture](https://img.shields.io/badge/architecture-Zero--Trust%20%7C%20Envelope%20Encryption-blue)](#)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](#)
[![License](https://img.shields.io/badge/license-Non--Commercial-orange)](#)

> **NEXUS-C2** to zdecentralizowana platforma orkiestracji autonomicznych agentów wykorzystująca zasady **Zero-Trust**, kryptograficzne szyfrowanie wiadomości (**Envelope Encryption / Web Crypto API**) oraz silnik **Deterministycznego Budżetowania Tokenów/Kontekstu**.

---

## 🏗️ Architektura Systemu

```mermaid
graph TD
    classDef crypto fill:#4a5568,stroke:#cbd5e0,stroke-width:1px,color:#fff;
    classDef agent fill:#2b6cb0,stroke:#90cdf4,stroke-width:2px,color:#fff;

    ControlPlane["Control Plane / Orchestrator"]
    AgentA["Worker Agent Alpha"]
    AgentB["Worker Agent Beta"]

    ControlPlane -->|Encrypted Payload| AgentA
    ControlPlane -->|Encrypted Payload| AgentB
    AgentA -.->|Peer-to-Peer Verification| AgentB

    class ControlPlane crypto;
    class AgentA,AgentB agent;