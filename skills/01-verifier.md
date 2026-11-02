---
skill_id: verifier
version: v1.0
status: active
description: Verify signatures
tools: [{name: verify_sig, path: tools/verify.py, deterministic: true}]
instructions: |
  step_id: verify
  tool: verify_sig
---
