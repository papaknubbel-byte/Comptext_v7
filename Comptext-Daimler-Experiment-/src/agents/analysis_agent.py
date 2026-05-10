"""
AnalysisAgent – LLM-Inference for industrial process analysis (CompText V7)
Engineered for zero-trust, scalability, and extreme diagnostic fidelity.
"""

from __future__ import annotations

import json
import re
import time
import os
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from src.agents.triage_agent import TriageResult
from src.core.kvtc import KVTCResult
from src.models.schemas import Analyseergebnis, EingabeDokument, ProcessPriority
from src.core.memory.kvtc_memory import KVTCPersistentMemory
from src.utils.logging import get_logger

_log = get_logger("comptext.analysis_agent")


class ModelBackend(StrEnum):
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    MOCK = "mock"


@dataclass
class AnalysisConfig:
    backend: ModelBackend = ModelBackend.MOCK
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    gemini_model: str = "gemini-2.0-flash"
    max_tokens: int = 1024
    temperature: float = 0.0  # V7: Force absolute determinism for industrial safety


_SYSTEM_PROMPT = """\
Du bist ein Experten-KI-System für Daimler Buses Prozessanalyse.
DEINE AUFGABE: Analysiere den komprimierten [KVTC-FRAME].
WICHTIG: Der Frame enthält mehrere UNABHÄNGIGE Incidents (getrennt durch ||).
REGEL: Du MUSSST für JEDEN Incident/Domäne mindestens einen Fakt im JSON berichten.

JSON-Schema:
{
  "zusammenfassung": "string",
  "massnahmen": ["string"],
  "erkannte_fehlercodes": ["string"],
  "konfidenz": float,
  "prioritaet_bestaetigung": "P1_KRITISCH | P2_DRINGEND | P3_ROUTINE"
}
"""

_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


class AnalysisAgent:
    def __init__(
        self,
        config: AnalysisConfig | None = None,
        cache: Any | None = None,
        memory: KVTCPersistentMemory | None = None,
    ) -> None:
        self._config = config or AnalysisConfig()
        self._cache = cache
        self._anthropic_client: Any = None
        self._memory = memory or KVTCPersistentMemory()
        self._gemini_client: Any = None

    async def analyze(
        self,
        dokument: EingabeDokument,
        kvtc: KVTCResult,
        triage: TriageResult,
    ) -> Analyseergebnis:
        if self._cache is not None:
            cached = self._cache.get(kvtc.checksum)
            if cached is not None:
                return cached

        t0 = time.perf_counter()
        memory_hits = self._memory.retrieve_relevant(dokument.doc_type.value)
        prompt = self._build_prompt(dokument, kvtc, triage)
        
        # V7: Systematic Async Inferenz via SDK
        raw_output = await self._infer_async(prompt)
        parsed = self._parse_output(raw_output, triage.prioritaet)

        result = Analyseergebnis(
            eingabe_checksum=kvtc.checksum,
            prioritaet=parsed.get("prioritaet", triage.prioritaet),
            zusammenfassung=parsed.get("zusammenfassung", ""),
            massnahmen=parsed.get("massnahmen", []) + ([f"memory_contexts={len(memory_hits)}"] if memory_hits else []),
            erkannte_fehlercodes=parsed.get("erkannte_fehlercodes", []),
            konfidenz=float(parsed.get("konfidenz", 0.7)),
            modell_id=(
                self._config.anthropic_model if self._config.backend == ModelBackend.ANTHROPIC 
                else (self._config.gemini_model if self._config.backend == ModelBackend.GEMINI else "mock")
            ),
            latenz_ms=round((time.perf_counter() - t0) * 1000, 3),
            rohausgabe=raw_output,
            token_original=kvtc.original_tokens,
            token_komprimiert=kvtc.compressed_tokens,
        )

        if self._cache is not None:
            self._cache.put(kvtc.checksum, result)

        return result

    def _build_prompt(self, dokument: EingabeDokument, kvtc: KVTCResult, triage: TriageResult) -> str:
        return (
            f"DOKUMENT-TYP: {dokument.doc_type.value}\n"
            f"KOMPRIMIERTES FRAME:\n{kvtc.frame}\n\n"
            "Erstelle eine strukturierte JSON-Analyse."
        )

    async def _infer_async(self, prompt: str) -> str:
        if self._config.backend == ModelBackend.ANTHROPIC:
            return await self._anthropic_sdk_infer(prompt)
        if self._config.backend == ModelBackend.GEMINI:
            return await self._gemini_sdk_infer(prompt)
        return self._mock_infer(prompt)

    async def _anthropic_sdk_infer(self, prompt: str) -> str:
        try:
            from anthropic import AsyncAnthropic
            if not self._anthropic_client:
                self._anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            message = await self._anthropic_client.messages.create(
                model=self._config.anthropic_model,
                max_tokens=self._config.max_tokens,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
                temperature=self._config.temperature,
            )
            return message.content[0].text
        except Exception as e:
            _log.error(f"Anthropic SDK error: {e}")
            return json.dumps({"zusammenfassung": f"Error: {e}", "konfidenz": 0.0})

    async def _gemini_sdk_infer(self, prompt: str) -> str:
        try:
            from google import genai
            if not self._gemini_client:
                # V7 uses explicit client initialization
                self._gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            
            response = await self._gemini_client.models.generate_content(
                model=self._config.gemini_model,
                contents=f"{_SYSTEM_PROMPT}\n\n{prompt}"
            )
            return response.text
        except Exception as e:
            _log.error(f"Gemini SDK error: {e}")
            return json.dumps({"zusammenfassung": f"Error: {e}", "konfidenz": 0.0})

    def _mock_infer(self, prompt: str) -> str:
        return json.dumps({
            "zusammenfassung": "V7 Mock: Deterministic industrial analysis.",
            "massnahmen": ["Nominal action"],
            "erkannte_fehlercodes": [],
            "konfidenz": 1.0,
            "prioritaet_bestaetigung": "P3_ROUTINE"
        })

    def _parse_output(self, raw: str, fallback_priority: ProcessPriority) -> dict[str, Any]:
        match = _JSON_BLOCK.search(raw)
        if not match:
            return {"zusammenfassung": raw[:300], "prioritaet": fallback_priority}
        try:
            data = json.loads(match.group(0))
            prio_str = data.get("prioritaet_bestaetigung", fallback_priority.value)
            data["prioritaet"] = ProcessPriority(prio_str) if prio_str in ProcessPriority._value2member_map_ else fallback_priority
            return data
        except:
            return {"zusammenfassung": raw[:300], "prioritaet": fallback_priority}
