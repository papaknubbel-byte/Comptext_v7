"""
Telemetry Events – Normalized schemas for Tinybird reporting.
"""

from typing import Any, Dict
from dataclasses import dataclass, asdict, field
import time

@dataclass
class TelemetryEvent:
    event_type: str
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PipelineEvent:
    endpoint: str
    original_tokens: int
    compressed_tokens: int
    savings_percentage: float
    latency_ms: float
    status: str = "success"
    event_type: str = "pipeline_execution"

@dataclass
class CompressionEvent:
    algorithm: str = "KVTC-V6"
    ratio: float = 0.0
    original_bytes: int = 0
    compressed_bytes: int = 0
    event_type: str = "compression_stats"

@dataclass
class CopilotSyncEvent:
    sync_status: str
    document_id: str
    latency_ms: float
    event_type: str = "copilot_sync"

@dataclass
class AuditEvent:
    action: str
    actor: str = "system"
    outcome: str = "allowed"
    event_type: str = "security_audit"
