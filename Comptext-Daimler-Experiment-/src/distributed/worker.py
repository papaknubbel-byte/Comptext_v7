"""
Worker Nodes – Decoupled processing units for CompText V7.
"""

import asyncio
import logging
import time
from src.core.kvtc import IndustrialKVTCStrategy
from src.agents.analysis_agent import AnalysisAgent
from src.agents.triage_agent import TriageAgent
from .models import EventType, TelemetryEvent, CompressedFrameEvent, IntelligenceInsightEvent
from .broker import broker
from .cache import cache

log = logging.getLogger("comptext.distributed.worker")

class CompressionWorker:
    def __init__(self):
        self.strategy = IndustrialKVTCStrategy()
        self.triage = TriageAgent()

    async def start(self):
        broker.subscribe(EventType.INGEST_RAW, self.handle_ingest)
        log.info("Compression Worker started.")

    async def handle_ingest(self, event: TelemetryEvent):
        # OTel Context established
        log.info(f"Processing Ingest: {event.event_id} (Trace: {event.trace_id})")
        
        if event.payload == "!!TRIGGER_ERROR!!":
            raise ValueError("Simulated Poison Pill")
        doc = EingabeDokument(raw_text=event.payload, doc_type=DocumentType.FREITEXT)
        triage_res = self.triage.classify(doc)
        
        t0 = time.perf_counter()
        kvtc_res = await asyncio.to_thread(
            self.strategy.compress, 
            event.payload, 
            priority=triage_res.prioritaet.value
        )
        latency = (time.perf_counter() - t0) * 1000
        
        # Phase 4 Metrics Injection
        event.metrics["comp_latency_ms"] = latency
        event.metrics["scr"] = kvtc_res.scr
        
        out_event = CompressedFrameEvent(
            parent_id=event.event_id,
            trace_id=event.trace_id, # Propagation
            frame=kvtc_res.frame,
            scr=kvtc_res.scr,
            dss=kvtc_res.dss,
            metrics=event.metrics,
            source="worker.compression"
        )
        await broker.publish(EventType.COMPRESSED_FRAME, out_event)

class InferenceWorker:
    def __init__(self):
        self.agent = AnalysisAgent()
        self._circuit_open = False

    async def start(self):
        broker.subscribe(EventType.COMPRESSED_FRAME, self.handle_compressed)
        log.info("Inference Worker started.")

    async def handle_compressed(self, event: CompressedFrameEvent):
        if self._circuit_open:
            log.warning("Circuit Breaker OPEN. Skipping inference.")
            return

        log.info(f"Processing Inference: {event.event_id} (Trace: {event.trace_id})")
        
        from src.models.schemas import EingabeDokument, DocumentType
        from src.core.kvtc import KVTCResult
        from src.agents.triage_agent import TriageResult
        from src.models.schemas import ProcessPriority
        
        doc = EingabeDokument(raw_text="", doc_type=DocumentType.FREITEXT)
        kvtc = KVTCResult(
            original_tokens=0, compressed_tokens=0, compression_ratio=1.0, 
            zones={}, frame=event.frame, checksum="abc", latency_ms=0.0
        )
        triage = TriageResult(prioritaet=ProcessPriority.P3_ROUTINE, begruendung="Worker Context", ausgeloeste_regeln=[])

        t0 = time.perf_counter()
        try:
            analyse_res = await self.agent.analyze(doc, kvtc, triage)
            latency = (time.perf_counter() - t0) * 1000
            
            # Phase 4 Metrics: Cost Savings Calculation
            # gpt-4o-mini approx cost: $0.15 / 1M tokens
            tokens_saved = 100 # Hypothetical for this event
            cost_saved = (tokens_saved / 1_000_000) * 0.15
            
            event.metrics["inf_latency_ms"] = latency
            event.metrics["usd_saved"] = cost_saved

            out_event = IntelligenceInsightEvent(
                parent_id=event.event_id,
                trace_id=event.trace_id, # Propagation
                priority=analyse_res.prioritaet,
                summary=analyse_res.zusammenfassung,
                actions=analyse_res.massnahmen,
                cfi=kvtc.cfi,
                metrics=event.metrics,
                source="worker.inference"
            )
            await broker.publish(EventType.INTELLIGENCE_INSIGHT, out_event)
        except Exception as e:
            log.error(f"Inference failure: {e}")
            # V7 Chaos Engineering: Partial outage logic would go here
            raise e # Trigger broker retry
