---
skill_id: reader
version: v1.0
status: active
description: Read-only source scanner
tools: [{name: ast, path: tools/ast.py, deterministic: true}]
instructions: |
  step_id: scan
  tool: ast
---
