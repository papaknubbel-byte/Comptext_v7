"""
Message Broker – Abstracted event bus for CompText V7.
Simulates a distributed broker (Kafka/NATS) using asyncio.Queue for local V7 testing.
"""

import asyncio
import logging
from enum import StrEnum
from typing import Callable, Dict, List
from .models import BaseEvent

log = logging.getLogger("comptext.distributed.broker")

class EventType(StrEnum):
    INGEST_RAW = "telemetry.raw.ingest"
    COMPRESSED_FRAME = "telemetry.compressed.frames"
    INTELLIGENCE_INSIGHT = "telemetry.intelligence.insights"
    FAILED_DLQ = "telemetry.failed.dlq" # Dead Letter Queue

class MessageBroker:
    def __init__(self):
        self._topics: Dict[str, asyncio.Queue] = {}
        self._subscribers: Dict[str, List[Callable]] = {}
        self.max_retries = 3

    async def publish(self, topic: str, event: BaseEvent):
        """
        Publishes an event with OTel trace propagation.
        """
        log.info(f"PUB [{topic}] ID={event.event_id} | TRACE={event.trace_id}")
        if topic not in self._topics:
            self._topics[topic] = asyncio.Queue()
        
        await self._topics[topic].put(event)
        
        if topic in self._subscribers:
            for sub in self._subscribers[topic]:
                # V7 Reliability: Encapsulated Execution with Retry
                asyncio.create_task(self._safe_execute(sub, topic, event))

    async def _safe_execute(self, handler: Callable, topic: str, event: BaseEvent):
        try:
            await handler(event)
        except Exception as e:
            log.error(f"Handler {handler.__name__} failed on {topic}: {e}")
            if event.retry_count < self.max_retries:
                event.retry_count += 1
                event.error_log.append(str(e))
                # Exponential backoff
                wait = 2 ** event.retry_count
                log.info(f"Retrying event {event.event_id} in {wait}s...")
                await asyncio.sleep(wait)
                await self.publish(topic, event)
            else:
                log.critical(f"Event {event.event_id} reached max retries. Routing to DLQ.")
                await self.publish(EventType.FAILED_DLQ, event)

    def subscribe(self, topic: str, handler: Callable):
        """
        Subscribes a handler to a specific topic.
        """
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)
        log.info(f"SUB [{topic}]: {handler.__name__}")

# Local instance
broker = MessageBroker()
