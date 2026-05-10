"""
Semantic Mapper – Convert CompText outputs into Copilot-compatible schema.
"""

from typing import Any, List, Optional
from pydantic import BaseModel, Field

from .resolver import resolve_comptext_uri
from src.interpretability.nla_stub import generate_explanation

class CopilotAttachment(BaseModel):
    title: str
    content: str
    explanation: str
    confidence: float
    anchors: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

def map_to_copilot(comptext_result: Any) -> CopilotAttachment:
    """
    Maps a CompText AnalysisResult or similar into a CopilotAttachment.
    Utilizes NLA (Natural Language Abstraction) for the explanation.
    """
    # Prepare NLA context
    nla_context = {
        "priority": getattr(comptext_result, "prioritaet", "Unknown"),
        "confidence": getattr(comptext_result, "konfidenz", 0.0),
        "codes": getattr(comptext_result, "erkannte_fehlercodes", []),
        "summary": getattr(comptext_result, "zusammenfassung", "")
    }
    
    analysis_id = getattr(comptext_result, "eingabe_checksum", "00000000")
    explanation = generate_explanation(analysis_id, nla_context)
    
    title = getattr(comptext_result, "zusammenfassung", "CompText Analysis")[:100]
    content = getattr(comptext_result, "rohausgabe", "No raw output available")
    
    return CopilotAttachment(
        title=title,
        content=content,
        explanation=explanation,
        confidence=nla_context["confidence"],
        anchors=nla_context["codes"],
        metadata={
            "model_id": getattr(comptext_result, "modell_id", "unknown"),
            "token_reduction": getattr(comptext_result, "token_einsparung_pct", 0.0),
            "uri": f"comptext://diagnostics/{analysis_id[:8]}"
        }
    )
