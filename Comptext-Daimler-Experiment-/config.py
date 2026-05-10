"""
Zentrale Konfiguration – Daimler Buses CompText
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from src.agents.analysis_agent import AnalysisConfig, ModelBackend


@dataclass
class AppConfig:
    # LLM-Backend
    analysis: AnalysisConfig = field(
        default_factory=lambda: AnalysisConfig(
            backend=ModelBackend(os.getenv("LLM_BACKEND", ModelBackend.MOCK.value)),
            model_id=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            claude_cli_model=os.getenv("CLAUDE_MODEL", "sonnet"),
            max_tokens=int(os.getenv("MAX_TOKENS", "512")),
            temperature=float(os.getenv("TEMPERATURE", "0.1")),
        )
    )

    # KVTC-Zonen
    kvtc_header_lines: int = int(os.getenv("KVTC_HEADER_LINES", "10"))
    kvtc_window_lines: int = int(os.getenv("KVTC_WINDOW_LINES", "15"))

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


DEFAULT_CONFIG = AppConfig()
