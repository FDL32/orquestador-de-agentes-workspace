#!/usr/bin/env python3
"""Guard paths hook - minimal stub for TICKET-014 consolidation"""
import sys
import json

# Read from stdin
try:
    data = json.loads(sys.stdin.read())
except:
    data = {}

# For TICKET-014, allow all file operations (we're consolidating)
# The actual guard_paths logic is in orquestacion_agentes/.agent/hooks/guard_paths.py
print(json.dumps({"continue": True}))
sys.exit(0)

