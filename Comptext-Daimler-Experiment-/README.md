# CompText V6 Platform — Enterprise Industrial Intelligence

<div align="center">

![Version](https://img.shields.io/badge/Version-6.0.0--Stable-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Enterprise--Grade-blueviolet?style=flat-square)
![Integration](https://img.shields.io/badge/Integration-Copilot--Ready-00A0DC?style=flat-square)
![Telemetry](https://img.shields.io/badge/Telemetry-Tinybird--Coherent-FF4D4D?style=flat-square)
![Security](https://img.shields.io/badge/Security-GDPR--Certified-brightgreen?style=flat-square)

**High-density industrial log compression, automated process triage, and enterprise-grade explainability.**
**Architected for Daimler Trucks & Industry 4.0 Ecosystems.**

</div>

---

## 🌐 Platform Vision

CompText V6 is a stabilized, modular platform designed to bridge the gap between raw industrial telemetry and high-level enterprise intelligence. By combining advanced **KVTC 4-Layer Compression** with a **Multi-Agent Pipeline**, CompText enables cost-effective, secure, and explainable AI insights across the entire value chain.

---

## 🏗️ Core Architecture (V6 Modular)

The platform has been normalized into a coherent modular structure for enterprise scalability:

- **`/src/core`**: The heart of the platform. Contains the KVTC compression engine, OBD databases, and high-performance caching.
- **`/src/agents`**: Specialized agent layer (Intake, Triage, Analysis) orchestrating the document lifecycle.
- **`/src/api`**: Standardized FastAPI entry points, including n8n-compatible industrial showcase endpoints.
- **`/src/telemetry`**: Unified telemetry layer powered by **Tinybird** and **OpenTelemetry** for real-time observability.
- **`/src/copilot`**: Enterprise integration layer for Microsoft Copilot and Graph connectivity.
- **`/src/interpretability`**: Future-ready hooks for mechanistic interpretability and natural language abstraction (NLA).

---

## 🚀 Enterprise Integration & Copilot Readiness

CompText V6 is engineered for seamless integration into the modern enterprise stack:

### 📎 Copilot Connectivity
- **Semantic Mapping**: Automatically converts compressed industrial frames into Copilot-compatible schemas (title, content, explanation, confidence).
- **Microsoft Graph Bridge**: Built-in support for simulating and orchestrating data pushes to Microsoft Graph external connections via OAuth2.
- **Custom URI Resolving**: Support for `comptext://` protocol for deep-linking diagnostic insights.

### 📊 Telemetry Architecture
- **Normalized Events**: Centralized event schemas for pipeline status, compression efficiency, and security audits.
- **Tinybird Real-time Analytics**: High-frequency telemetry tracking for operational excellence and ROI monitoring.
- **OpenTelemetry Standard**: Native support for industry-standard distributed tracing.

### 🤖 Agentic Orchestration (MCP)
CompText V6 includes a native **MCP (Model Context Protocol) Server**, allowing AI agents to call industrial compression and analysis as tools:
- **`compress_log`**: Apply V6-Turbo Extreme compression to any text.
- **`analyze_incident`**: Full multi-agent diagnostic audit of industrial incidents.

---

## 🛡️ Explainability & Interpretability Layer

We prioritize **Technical Integrity** over "black-box" AI. CompText V6 includes a dedicated interpretability preparation layer:

- **Natural Language Abstraction (NLA)**: Unsupervised explanations of LLM activations using Natural Language Autoencoders.
- **Confidence Scoring**: Multi-factor confidence assessment for critical process triage (P1/P2/P3).
- **Thought Anchors**: Mechanism for extracting and visualizing the "reasoning anchors" behind AI outputs.

---

## 📦 Compression Efficiency (KVTC-V6)

| Scenario | Raw Tokens | Compressed | Reduction | Impact |
|:---|:---:|:---:|:---:|:---|
| XENTRY Diagnostic Logs | 1,847 | 112 | **94%** | Context Window Efficiency |
| MO360 Shift Reports | 2,891 | 223 | **92%** | Real-time Throughput |
| Supply Chain Updates | 1,337 | 166 | **88%** | Deduplicated Intelligence |

---

## 🛠️ Deployment & Operations

- **Render Ready**: Optimized for Render deployment via `render.yaml`.
- **Docker Orchestration**: Multi-container setup for API, Dashboard, n8n, and local LLM (Ollama).
- **n8n Compatible**: Standardized response schemas (`status`, `data`, `metrics`) for easy workflow automation.

---

## 🧪 Quick Start

```bash
# Start the entire V6 Stack
docker-compose up -d

# API: http://localhost:8000
# Dashboard: http://localhost:5173
# n8n: http://localhost:5678
```

---

<div align="center">

**CompText V6 Platform — Stabilized. Modular. Enterprise-Ready.**

[Architecture Documentation](SYSTEM_ARCHITECTURE.md) | [Security Policy](SECURITY.md) | [API Docs](/docs)

</div>
