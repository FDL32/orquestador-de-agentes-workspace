# RUNTIME_EXCLUSIONS Configuration

**Purpose:** Define files that should NOT be packaged/distributed with agent_system

**Implementation:** These files remain in agent_system/ but are marked as RUNTIME (not PLANTILLA)

---

## Files to Exclude from Packaging

### agent_system/.agent/collaboration/
- `STATE.md` - Live project state
- `TURN.md` - Current agent turn state
- `execution_log.md` - Execution history
- `.session_state.json` - Session metadata
- `.tool_counter.json` - Tool usage tracking

## Implementation Notes

### For install_agent_system.py
When distributing agent_system, use this ignore pattern:

```python
ignore_patterns = [
    '.agent/collaboration/STATE.md',
    '.agent/collaboration/TURN.md',
    '.agent/collaboration/execution_log.md',
    '.agent/collaboration/.session_state.json',
    '.agent/collaboration/.tool_counter.json',
    '.pytest_cache/',
    '__pycache__/',
    '*.pyc',
]
```

### For upgrade_agent_system.py
Preserve existing runtime files when upgrading:

```python
preserve_runtime = [
    '.agent/collaboration/STATE.md',
    '.agent/collaboration/TURN.md',
    '.agent/collaboration/execution_log.md',
]
```

### For packaging/distribution
When creating a distribution archive:

```bash
tar --exclude='.agent/collaboration/STATE.md' \
    --exclude='.agent/collaboration/TURN.md' \
    --exclude='.agent/collaboration/execution_log.md' \
    -czf agent_system.tar.gz agent_system/
```

---

## Verification

Run this to verify RUNTIME files are not included:

```bash
python scripts/install_agent_system.py --verify-exclusions
```

---

## Related Documents

- TICKET-013-REDUNDANCY-ANALYSIS.md (Authority map)
- TICKET-014-SPEC.md (Implementation plan)
- agent_system/README.md (Updated framework description)

