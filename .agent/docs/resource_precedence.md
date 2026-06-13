# Resource Precedence for Host-Extends / Motor-Provides

Date verified: 2026-06-13
Destination HEAD: `13ee7e1`
Motor HEAD: `704939f`

## Objective

This document fixes the canonical resource resolution order for `repo_destino`
and maps each currently known destination command that still points to a local
copy or stale local path.

This is the A2a deliverable for `WOT-AUDIT-A2a`. It is documentation only.
It does not move, delete, or repoint files.

## Resolution Order

Resource resolution for skills, prompts, scripts, and tools follows this
precedence:

1. Host-local extensions in `repo_destino/.agent/{skills,prompts,tools}/`
2. External motor resources in `repo_motor/{skills,prompts,scripts}/`
3. Legacy installed copies in `repo_destino/{scripts,skills,agent_system}/`

The third level is transitional only. Once an equivalent external-motor
invocation exists, legacy copies are not a valid steady-state resolution path.

If the destination needs behavior that differs from the motor, it must add its
own host-local resource under `.agent/`. It must not edit a motor skill, prompt,
or script in place from the destination.

## Operational Notes

- `AGENT_PROJECT_ROOT` is the real project-root propagation channel used by the
  motor runtime.
- Some motor scripts also depend on `cwd=<repo_destino>` for host-first
  discovery and guard-path behavior.
- The shorthand pattern `python <repo_motor>/scripts/X.py --project-root
  <repo_destino>` is not universally valid today. For A2b, each command must be
  repointed using the invocation shape its current motor entry point actually
  supports.

## Command Mapping

Evidence source:
- `.claude/settings.local.json`
- destination filesystem checks (`Test-Path`)
- motor script interface inspection
- safe runtime probes from `cwd=<repo_destino>` with
  `AGENT_PROJECT_ROOT=<repo_destino>`

| Current destination command | Current local status | Motor equivalent status | External-motor invocation shape verified for A2b |
| --- | --- | --- | --- |
| `python scripts/run_pytest_safe.py` | Local legacy copy exists in destination | Motor script exists | `Set-Location <repo_destino>` + `AGENT_PROJECT_ROOT=<repo_destino>` + `python <repo_motor>/scripts/run_pytest_safe.py --status` verified. The script does not expose `--project-root`; root resolution comes from env var. |
| `python scripts/discover_skills.py --json` | Local legacy copy exists in destination | Motor script exists | `Set-Location <repo_destino>` + `AGENT_PROJECT_ROOT=<repo_destino>` + `python <repo_motor>/scripts/discover_skills.py --json` verified. Host-first discovery depends on `cwd` for `.agent/skills`; no `--project-root` CLI exists. |
| `python scripts/local_audit.py --quick` | No local copy in destination | Motor script exists | `Set-Location <repo_destino>` + `AGENT_PROJECT_ROOT=<repo_destino>` + `python <repo_motor>/scripts/local_audit.py --json --quick` verified. The script does not accept `--project-root`; root resolution comes from env var. |
| `python scripts/test_refactor_kit_performance.py` | Local legacy copy exists in destination | Motor equivalent exists at `tests/test_refactor_kit_performance.py` (run by the pytest suite via `run_pytest_safe.py`) | CORRECTION (2026-06-13): the original A2a claim "no equivalent" was a verification gap (only `scripts/` was checked). The destino copy is the same test as the motor's, differing only in a BOM, a `# ruff: noqa: PERF203` line, and the trailing newline -- a functionally corresponding test exists in the motor, so there is no capability gap. No motor promotion or host reclassification is needed: A2b drops the stale destino copy and its allowlist entry; coverage is preserved by the motor suite. Not a real STOP. |
| `python agent_system/refactor-kit/install_refactor_kit.py /tmp/test_refactor_project` | Referenced path is stale: `refactor-kit` with hyphen is absent in destination | Motor has `agent_system/refactor_kit/install_refactor_kit.py` with underscore | Current allowlist entry is dead and must be cleaned in A2b. The external equivalent must use the underscore path, not the hyphen path. |

## STOP Conditions for A2b

1. ~~`scripts/test_refactor_kit_performance.py` has no motor equivalent.~~
   RESOLVED / NOT A STOP (corrected 2026-06-13): the motor has the equivalent
   test at `tests/test_refactor_kit_performance.py`, exercised by the pytest
   suite (`run_pytest_safe.py`). The original "no equivalent" finding only
   inspected `scripts/`. A2b simply drops the stale destino copy and its
   allowlist entry; no motor capability decision is required.
2. `agent_system/refactor-kit/install_refactor_kit.py` is a stale allowlist
   entry. A2b must clean or replace it explicitly; it cannot be treated as a
   valid command path.
3. If any additional destination command is found to depend on a legacy copy
   without a verified motor invocation shape, it must be added here and handled
   as a STOP instead of being repointed speculatively.

## Scope Boundary

- A2a does not modify `.claude/settings.local.json`.
- A2a does not archive or delete legacy copies.
- A2a does not change motor prompts, skills, or scripts.
- A2b and later phases own repointing, clone-clean validation, and legacy
  removal.
