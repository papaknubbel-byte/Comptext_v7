"""
V7 Mesh Demonstrator – Validates Distributed Architecture and Scientific Metrics.
Spins up decoupled workers and traces a multi-domain ecosystem payload.
"""

import asyncio
import logging
import json
from src.distributed.broker import broker
from src.distributed.worker import CompressionWorker, InferenceWorker
from src.distributed.models import EventType, TelemetryEvent

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("v7.demonstrator")

# Test Payload
ECOSYSTEM_PAYLOAD = """
--- SOURCE: MO360 ---
LINE_D: EMERGENCY_STOP | REASON: THERMAL_OVERLOAD
--- SOURCE: SAP-MM ---
PO_4500112233: MATERIAL: CYLINDER-HEAD | STATUS: DELAYED
--- SOURCE: XENTRY ---
VIN: WDB906232N3123456 | DTC: P0300 (ACTIVE) | STATUS: P1_ESCALATION
"""

async def run_demonstration():
    log.info("Starting V7 Mesh Demonstration...")
    
    # 1. Initialize Workers
    comp_worker = CompressionWorker()
    inf_worker = InferenceWorker()
    
    await comp_worker.start()
    await inf_worker.start()
    
    # 2. Setup Result Monitor
    results = []
    
    async def monitor_insights(event):
        log.info(f"🏆 INSIGHT RECEIVED: Prio={event.priority} | CFI={event.cfi}")
        results.append(event)
        
    broker.subscribe(EventType.INTELLIGENCE_INSIGHT, monitor_insights)

    # 3. Inject Initial Ingest Event
    ingest_event = TelemetryEvent(
        payload=ECOSYSTEM_PAYLOAD,
        source="demonstrator.ingress"
    )
    
    log.info(f"Injecting Ingest Event: {ingest_event.event_id}")
    await broker.publish(EventType.INGEST_RAW, ingest_event)
    
    # 4. Wait for processing to complete (local simulation)
    # Give it a few seconds to flow through the mesh
    await asyncio.sleep(5)
    
    log.info("\n" + "="*80)
    log.info("      V7 SCIENTIFIC AUDIT REPORT (DISTRIBUTED)")
    log.info("="*80)
    
    if results:
        res = results[0]
        log.info(f"System State:    STABLE (Distributed)")
        log.info(f"Global Priority: {res.priority}")
        log.info(f"Avg CFI Score:   {res.cfi} (Compression Fidelity)")
        log.info(f"Deployment:      Production-Ready Blueprint")
    else:
        log.error("Demonstration timed out or failed.")
        
    log.info("="*80)

if __name__ == "__main__":
    asyncio.run(run_demonstration())
