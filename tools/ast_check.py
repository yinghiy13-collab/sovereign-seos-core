#!/usr/bin/env python3
import ast, json, sys, argparse
from pathlib import Path

FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__"}
FORBIDDEN_MODULES = {"subprocess", "ctypes", "socket"}

def check_ast(filepath: Path):
    v = []
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError) as e:
        return [{"file": str(filepath), "line": getattr(e, "lineno", 0), "issue": f"ParseError: {e}"}]
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
            v.append({"file": str(filepath), "line": node.lineno, "issue": f"Forbidden call: {node.func.id}"})
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            mods = [n.name for n in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for m in mods:
                if m.split(".")[0] in FORBIDDEN_MODULES:
                    v.append({"file": str(filepath), "line": node.lineno, "issue": f"Forbidden module: {m}"})
    return v

def scan(target: Path):
    files = sorted(target.rglob("*.py")) if target.is_dir() else []
    if not files:
        return None, [{"file": str(target), "line": 0, "issue": "NO_EVIDENCE: nothing to scan"}]
    out = []
    for f in files:
        out.extend(check_ast(f))
    return files, out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--target", default="tools")
    a = p.parse_args()
    files, viol = scan(Path(a.target))
    status = "PASS" if not viol else "FAIL"
    rep = {"status": status, "violations": viol, "scanned_dir": a.target,
           "files_scanned": [str(f) for f in files or []]}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(f"AST Check: {status} ({len(viol)} violations, {len(files or [])} files)")
    sys.exit(0 if status == "PASS" else 1)

if __name__ == "__main__":
    main()
