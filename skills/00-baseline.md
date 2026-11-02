---
skill_id: baseline-verifier
version: v1.0
status: trial
description: Minimal baseline verifier
tools: [{name: check_skill, path: scripts/check_skill.py, deterministic: true}]
instructions: |
  step_id: verify
  tool: check_skill
---
