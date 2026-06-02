# Agent System Upgrade Guide

Complete reference for upgrading existing z_scripts projects to the latest version.

---

## Quick Start

```bash
# Step 1: Detect current version
python scripts/detect_agent_system_version.py .

# Step 2: Dry-run (see what would change)
python scripts/upgrade_agent_system.py . --dry-run

# Step 3: Actual upgrade (automatic backup created)
python scripts/upgrade_agent_system.py . --confirm

# Step 4: Verify (optional, recommended)
python scripts/upgrade_agent_system.py . --verify
```

---

## Understanding Versions

### Version Detection Strategy

The system uses **pattern-based version detection** rather than folder names. Each version has
a set of required markers (files/directories that must exist):

| Version | Required Markers | Key Features |
|---------|------------------|--------------|
| **v8.x** | `.agent/agent_controller.py`<br>`scripts/run_pytest_safe.py` | Base system, single agent |
| **v9.0-v9.1** | v8.x markers<br>`.agent/rules/`<br>`skills/` | Multi-agent support, skills system |
| **v9.2** | v9.0 markers<br>`agent_system/refactor_kit/` | Refactoring capability, portable toolkit |
| **v9.4** | v9.2 markers<br>`.claude/rules/`<br>`AGENTS.md` | Modular documentation, Claude Code native |

### Version Compatibility

```
v8.x â†’ v9.0-v9.1 â†’ v9.2 â†’ v9.4
 â”‚         â”‚         â”‚        â””â”€ Latest
 â”‚         â”‚         â””â”€ Can upgrade from v8.x or v9.0-v9.1
 â”‚         â””â”€ Can upgrade from v8.x
 â””â”€ Oldest supported version
```

---

## Upgrade Workflows

### Workflow 1: Standard Upgrade (Recommended)

**Scenario:** Most projects. Local changes exist (customized rules, skills).

```bash
# 1. Check current state
python scripts/detect_agent_system_version.py .
# Output:
# Detected Version: v9.0-v9.1
# Upgrade Path: v9.0-v9.1 â†’ v9.2 â†’ v9.4

# 2. Dry-run to see what would change
python scripts/upgrade_agent_system.py . --dry-run
# Output:
# Status: READY_FOR_UPGRADE
# Current Version: v9.0-v9.1
# Target Version: v9.4
# Upgrade Path: v9.0-v9.1 â†’ v9.2 â†’ v9.4
# Local Changes Detected:
#   modified: .agent/rules/
#   modified: skills/custom-skill/
#
# Dry run - no changes made. Run with --confirm to proceed.

# 3. Review local changes
# Look at modified files to ensure you want to preserve them:
git status .agent/rules/ skills/

# 4. Perform upgrade (creates automatic backup)
python scripts/upgrade_agent_system.py . --confirm
# Output:
# Status: COMPLETED
# Backup: .agent/backups/backup_20260426_160000
# merge_results: {updated: [...], requires_manual_merge: [...]}

# 5. Verify integrity
python scripts/upgrade_agent_system.py . --verify
# Output:
# Verification Status: âœ“ PASS
#   version_detected: v9.4
#   confidence: high
#   required_markers_met: True
#   no_conflicts: True
```

**Key Points:**
- Automatic backup created before any changes
- Local customizations preserved
- Three-way merge strategy handles conflicts
- Verification ensures integrity post-upgrade

---

### Workflow 2: Zero-Risk Dry-Run (Conservative Projects)

**Scenario:** High-risk environments. Need maximum visibility before proceeding.

```bash
# 1. Dry-run with detailed analysis
python scripts/upgrade_agent_system.py . --dry-run

# 2. Export plan to file for review
python scripts/upgrade_agent_system.py . --dry-run > upgrade_plan.txt

# 3. Review with team (email, PR comments, etc.)
cat upgrade_plan.txt

# 4. Once approved, proceed
python scripts/upgrade_agent_system.py . --confirm

# 5. Run full verification suite
python scripts/upgrade_agent_system.py . --verify
python scripts/detect_agent_system_version.py .
python scripts/run_pytest_safe.py  # Quality gates
```

---

### Workflow 3: Fast Upgrade (Non-Customized Projects)

**Scenario:** Stock installation, no local changes.

```bash
# Single command - confidence is high
python scripts/upgrade_agent_system.py . --confirm

# Verify immediately
python scripts/upgrade_agent_system.py . --verify
```

---

## Backup and Recovery

### Automatic Backups

Every upgrade creates an **automatic timestamped backup** before any changes:

```
.agent/backups/
â”œâ”€â”€ backup_20260426_160000/
â”‚   â”œâ”€â”€ .agent/
â”‚   â”œâ”€â”€ .claude/
â”‚   â”œâ”€â”€ skills/
â”‚   â”œâ”€â”€ scripts/
â”‚   â””â”€â”€ BACKUP_MANIFEST.json       â† Contains version info and recovery command
â”œâ”€â”€ backup_20260420_140530/
â””â”€â”€ backup_20260415_102000/
```

**Backup Manifest Example:**
```json
{
  "timestamp": "20260426_160000",
  "version_before": "v9.2",
  "critical_paths_backed_up": [...],
  "restoration_command": "python scripts/rollback_agent_system.py --backup 20260426_160000"
}
```

### List Available Backups

```bash
python scripts/rollback_agent_system.py --list
# Output:
# Available Backups (3):
#
#   ID: 20260426_160000
#      Version: v9.2
#      Paths: 8
#
#   ID: 20260420_140530
#      Version: v9.0-v9.1
#      Paths: 8
```

### Restore from Backup

**Restore latest backup:**
```bash
python scripts/rollback_agent_system.py --latest
```

**Restore specific backup:**
```bash
python scripts/rollback_agent_system.py --backup 20260426_160000
```

**Restore + Verify:**
```bash
python scripts/rollback_agent_system.py --backup 20260426_160000 --verify
# Output:
# Restore Status: COMPLETED
# Version Restored: v9.2
# Paths Restored: 8
#
# Verification: âœ“ PASS
#   version_detected: v9.2
#   integrity_ok: True
```

---

## Handling Local Customizations

### Local Customizable Paths

The upgrade process **preserves local changes** in these directories:

- `.agent/rules/` â€” Custom manager/builder rules
- `skills/` â€” Custom skills and integrations
- `CLAUDE.md` â€” Project-specific Claude Code configuration
- `PROJECT.md` â€” Project metadata and decisions

### Three-Way Merge Strategy

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚         LOCAL PROJECT STATE                 â”‚
â”‚  (Last backed-up or current state)          â”‚
â”‚                                             â”‚
â”‚  âœ“ Custom rules in .agent/rules/            â”‚
â”‚  âœ“ Custom skills in skills/                 â”‚
â”‚  âœ“ Local CLAUDE.md modifications            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
            â†“ THREE-WAY MERGE â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚      UPSTREAM SOURCE (z_scripts)            â”‚
â”‚  (New version being installed)              â”‚
â”‚                                             â”‚
â”‚  âœ“ Updated .agent/                          â”‚
â”‚  âœ“ Updated scripts/                         â”‚
â”‚  âœ“ New features in refactor-kit/            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
            â†“ CONFLICT RESOLUTION â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚      UPGRADED PROJECT STATE                 â”‚
â”‚  (Merged result)                            â”‚
â”‚                                             â”‚
â”‚  âœ“ New upstream files                       â”‚
â”‚  âœ“ LOCAL CHANGES PRESERVED â† Key Benefit    â”‚
â”‚  âœ“ Markers verified                         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Conflict Resolution

If merge detects local changes:

```bash
# Dry-run shows which paths require manual merge
python scripts/upgrade_agent_system.py . --dry-run
# Output:
# Local Changes Detected:
#   modified: .agent/rules/custom-rule.md
#   modified: skills/my-skill/SKILL.md
#
# Some paths require manual merge strategy selection:
#   - Review changes in .agent/rules/
#   - Decide: Keep local, accept upstream, or manual merge
#   - Run with --confirm to proceed

# For manual merge conflicts, you have options:
# 1. Keep local version (edit to skip update)
# 2. Accept upstream version (backup is saved)
# 3. Git three-way merge (if using version control)
```

**If You Need Manual Merge:**

```bash
# 1. Backup current state manually
cp -r .agent/rules .agent/rules.backup_manual

# 2. Inspect the source upgrade
ls -la /path/to/z_scripts/.agent/rules/

# 3. Merge carefully (editor or git)
git merge-tool .agent/rules/conflicting-file.md

# 4. Run verification after manual merge
python scripts/upgrade_agent_system.py . --verify
```

---

## Troubleshooting

### Problem 1: "Could not detect current version"

**Cause:** Project doesn't have recognizable agent system structure.

```bash
# Check what's present
ls -la .agent/ agent_system/ skills/ .claude/

# Try manual detection with more detail
python scripts/detect_agent_system_version.py . --verbose

# If system exists but isn't detected, project may be too old or corrupted
# Option 1: Fresh install (backup first)
python agent_system/scripts/install_agent_system.py . --reinit

# Option 2: Manual restoration from backup
python scripts/rollback_agent_system.py --latest
```

### Problem 2: "Verification failed after upgrade"

**Cause:** Merge created inconsistencies or broke required markers.

```bash
# 1. Automatic rollback is available
python scripts/rollback_agent_system.py --latest

# 2. Check verification details
python scripts/upgrade_agent_system.py . --verify
# Output shows:
# - Which markers are missing
# - Which conflicts remain
# - Specific files to investigate

# 3. If rollback doesn't help:
# - Manually restore critical files from backup
# - Run quality gates to identify issues
python scripts/run_pytest_safe.py
ruff check .agent/ --fix
```

### Problem 3: "Backup is corrupted or incomplete"

**Cause:** Filesystem issue during backup creation.

```bash
# 1. Check backup integrity
ls -la .agent/backups/backup_TIMESTAMP/
file .agent/backups/backup_TIMESTAMP/BACKUP_MANIFEST.json

# 2. Try different backup
python scripts/rollback_agent_system.py --list
python scripts/rollback_agent_system.py --backup EARLIER_TIMESTAMP

# 3. If no valid backup exists:
# - Use version control (git) to restore
# - Or reinstall from scratch
git log --oneline .agent/ agent_system/
git checkout <commit> .agent/ agent_system/
```

### Problem 4: "Merge strategy chose wrong version"

**Cause:** Three-way merge doesn't know user intent.

```bash
# 1. Understand what merged
python scripts/upgrade_agent_system.py . --verify
# Shows exactly which files were merged and how

# 2. Restore backup
python scripts/rollback_agent_system.py --latest

# 3. Do manual merge instead
# Copy new version, then selectively restore local changes
cp -r /path/to/z_scripts/.agent ./
# Now manually restore only custom files you need
git diff .agent/rules/ | patch -p1
```

---

## Best Practices

### Before Upgrade

- âœ“ Commit all changes to version control
- âœ“ Run quality gates (`ruff`, `pytest`, `pip-audit`)
- âœ“ Document your customizations in `PROJECT.md`
- âœ“ Review CHANGELOG between your version and target version
- âœ“ Do a dry-run first (`--dry-run`)

### During Upgrade

- âœ“ Run with `--confirm` only after dry-run approval
- âœ“ Automatic backup is created (always safe)
- âœ“ Watch for "requires_manual_merge" indicators
- âœ“ Let the script finish completely (don't interrupt)

### After Upgrade

- âœ“ Run verification (`--verify`)
- âœ“ Run quality gates (`/quality-gates` or manual)
- âœ“ Test key workflows (especially refactor-kit, skills)
- âœ“ Commit upgrade to version control
- âœ“ Document upgrade in CHANGELOG.md if doing multi-project upgrades

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Upgrade Agent System

on: [workflow_dispatch]

jobs:
  upgrade:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Detect version
        run: python scripts/detect_agent_system_version.py .
      
      - name: Dry-run upgrade
        run: python scripts/upgrade_agent_system.py . --dry-run
      
      - name: Perform upgrade
        run: python scripts/upgrade_agent_system.py . --confirm
      
      - name: Verify integrity
        run: python scripts/upgrade_agent_system.py . --verify
      
      - name: Run quality gates
        run: |
          python scripts/run_pytest_safe.py
          ruff check .agent/ --fix
      
      - name: Create PR with upgrade results
        uses: peter-evans/create-pull-request@v4
        with:
          title: "chore: Upgrade agent system"
          body: "Automated upgrade completed. See workflow for details."
```

---

## When to Upgrade

### Automatic (Recommended)

- Version detection is automatic
- Upgrade path is calculated automatically
- Merge strategy is automatic (three-way)
- Backup/recovery is automatic

**Result:** Safe, low-friction upgrades

### Manual (Rare)

- If automatic detection fails â†’ investigate root cause
- If merge strategy needs adjustment â†’ use rollback + manual merge
- If version mismatch suspected â†’ run `--verify` first

---

## Reference

| Tool | Purpose | Command |
|------|---------|---------|
| `detect_agent_system_version.py` | Version detection | `python scripts/detect_agent_system_version.py .` |
| `upgrade_agent_system.py` | Upgrade workflow | `python scripts/upgrade_agent_system.py . --confirm` |
| `rollback_agent_system.py` | Recovery/rollback | `python scripts/rollback_agent_system.py --latest` |
| `run_pytest_safe.py` | Quality gates | `python scripts/run_pytest_safe.py` |
| `orquestador.py` | Multi-agent orchestration | `python scripts/orquestador.py --stage plan` |

---

**Last Updated:** 2026-04-26  
**Status:** Production Ready (v9.4)

