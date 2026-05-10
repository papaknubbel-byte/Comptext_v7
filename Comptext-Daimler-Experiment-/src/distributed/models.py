"""
Distributed Models – Standardized event schemas for CompText V7.
"""

from enum import StrEnum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class EventType(StrEnum):
    INGEST_RAW = "telemetry.raw.ingest"
    COMPRESSED_FRAME = "telemetry.compressed.frames"
    INTELLIGENCE_INSIGHT = "telemetry.intelligence.insights"

class BaseEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4())) # OTel Trace Propagation
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = "unknown"
    version: str = "7.0.0"
    # Phase 5: Reliability metadata
    retry_count: int = 0
    error_log: List[str] = []
    
    # Phase 4: Observability metrics
    metrics: Dict[str, Any] = {}

class TelemetryEvent(BaseEvent):
    event_type: EventType = EventType.INGEST_RAW
    payload: str
    metadata: Dict[str, Any] = {}

class CompressedFrameEvent(BaseEvent):
    event_type: EventType = EventType.COMPRESSED_FRAME
    parent_id: str
    frame: str
    scr: float # Semantic Compression Ratio
    dss: float # Diagnostic Survivability Score
    metadata: Dict[str, Any] = {}

class IntelligenceInsightEvent(BaseEvent):
    event_type: EventType = EventType.INTELLIGENCE_INSIGHT
    parent_id: str
    priority: str
    summary: str
    actions: List[str]
    cfi: float # Compression Fidelity Index
    metadata: Dict[str, Any] = {}
