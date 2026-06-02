"""Tests de higiene para el EventBus."""

from __future__ import annotations

import json
import sys
from pathlib import Path


# El paquete vivo está en orquestador_de_agentes/; el nombre antiguo queda solo
# para trazabilidad histórica, no para imports operativos.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "orquestador_de_agentes"))

from bus.event_bus import EventBus


def _event(
    *,
    event_id: str,
    event_type: str,
    ticket_id: str,
    actor: str,
    sequence_number: int,
    payload: dict,
) -> dict:
    return {
        "event_id": event_id,
        "event_type": event_type,
        "ticket_id": ticket_id,
        "actor": actor,
        "timestamp": "2026-05-20T13:00:00+00:00",
        "payload": payload,
        "schema_version": "1.0",
        "sequence_number": sequence_number,
    }


def test_read_events_ignores_leading_blank_prefix(tmp_path):
    runtime_dir = tmp_path / "runtime"
    runtime_dir.mkdir()
    events_path = runtime_dir / "events.jsonl"
    events_path.write_text(
        "\r\n"
        + json.dumps(
            _event(
                event_id="evt-1",
                event_type="STATE_CHANGED",
                ticket_id="WP-2026-109",
                actor="SUPERVISOR",
                sequence_number=1,
                payload={"from_state": "IN_PROGRESS", "to_state": "READY_FOR_REVIEW"},
            ),
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    bus = EventBus(runtime_dir)

    records = bus.read_events()
    assert len(records) == 1
    assert records[0].event_type == "STATE_CHANGED"
    assert records[0].sequence_number == 1


def test_emit_appends_after_existing_events(tmp_path):
    runtime_dir = tmp_path / "runtime"
    runtime_dir.mkdir()
    events_path = runtime_dir / "events.jsonl"
    events_path.write_text(
        json.dumps(
            _event(
                event_id="evt-1",
                event_type="STATE_CHANGED",
                ticket_id="WP-2026-109",
                actor="SUPERVISOR",
                sequence_number=1,
                payload={"from_state": "IN_PROGRESS", "to_state": "READY_FOR_REVIEW"},
            ),
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    bus = EventBus(runtime_dir)
    emitted = bus.emit(
        "STATE_CHANGED",
        ticket_id="WP-2026-109",
        actor="SUPERVISOR",
        payload={"from_state": "IN_PROGRESS", "to_state": "READY_FOR_REVIEW"},
    )

    assert emitted is not None
    assert emitted.sequence_number == 2
    records = bus.read_events()
    assert len(records) == 2
    assert records[-1].sequence_number == 2
