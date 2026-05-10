"""CompText MCP Server tools for compression, analysis, and agent-loop tool execution."""

from __future__ import annotations

import asyncio
from mcp.server.fastmcp import FastMCP

from src.core.kvtc import IndustrialKVTCStrategy
from src.agents.intake_agent import IntakeAgent
from src.agents.triage_agent import TriageAgent
from src.agents.analysis_agent import AnalysisAgent

mcp = FastMCP("CompText-V8")
strategy = IndustrialKVTCStrategy()
intake = IntakeAgent()
triage = TriageAgent()
analysis = AnalysisAgent()


def run_analysis_pipeline(text: str, source: str = "MCP") -> dict:
    intake_res = intake.process(text, quelle=source)
    triage_res = triage.classify(intake_res.dokument)
    analysis_res = asyncio.run(analysis.analyze(intake_res.dokument, intake_res.kvtc, triage_res))
    return {
        "priority": analysis_res.prioritaet.value,
        "summary": analysis_res.zusammenfassung,
        "actions": analysis_res.massnahmen,
        "codes": analysis_res.erkannte_fehlercodes,
        "savings": f"{analysis_res.token_einsparung_pct}%",
    }


@mcp.tool()
def compress_log(text: str) -> str:
    return strategy.compress(text).frame


@mcp.tool()
def analyze_incident(text: str, source: str = "MCP") -> dict:
    try:
        return run_analysis_pipeline(text, source)
    except Exception as e:
        return {"error": str(e), "status": "failed"}


@mcp.tool()
def execute_agent_action(intent: str, state: dict) -> dict:
    if "analyze" in intent.lower() or state.get("tool_required"):
        return {"solution_found": True, "solution": run_analysis_pipeline(state.get("raw_text", intent), "AgentLoop")}
    return {"observation": "no-op tool", "confidence": state.get("confidence", 0.5)}


if __name__ == "__main__":
    mcp.run()
