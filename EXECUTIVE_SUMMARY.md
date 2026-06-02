# Executive Summary

`z_scripts/` is the meta-documentation and historical control plane for the repository.
The active portable multi-agent runtime lives in `orquestacion_agentes/`, with canonical state under `orquestacion_agentes/.agent/`.

## What this repository contains

- A portable multi-agent template for Builder, Manager, Supervisor, and review workflows.
- A root-level documentation layer that explains the architecture, version contract, and operating rules.
- A concrete runtime template under `orquestacion_agentes/` with its own `QUICKSTART.md`, `CLAUDE.md`, `AGENTS.md`, and canonical `.agent/` state.

## Where to start

If you want to run the system:

1. Read `orquestacion_agentes/QUICKSTART.md`.
2. Read `orquestacion_agentes/INTERACTION_MODES.md`.
3. Use the active ticket state under `orquestacion_agentes/.agent/collaboration/`.
4. Start Builder, Supervisor, and Review Bridge in separate terminals.

For the shortest path from the repository root, use `README.md` as the hub and jump from there to this summary or to `orquestacion_agentes/QUICKSTART.md`.

## Source of truth

- Root documents: meta-docs and historical decisions.
- `orquestacion_agentes/`: active runtime and copy-ready template.
- `orquestacion_agentes/.agent/collaboration/`: canonical operational state for the active template.
- `orquestacion_agentes/.agent/runtime/memory/`: persistent project memory.

## Current status

- Version: `v9.5`
- Template state: copy-ready
- Operating mode: terminal-driven workflows supported and documented

## Related docs

- `README.md`
- `PROJECT.md`
- `CHANGELOG.md`
- `orquestacion_agentes/QUICKSTART.md`
- `orquestacion_agentes/INTERACTION_MODES.md`
- `orquestacion_agentes/CLAUDE.md`
- `orquestacion_agentes/AGENTS.md`
