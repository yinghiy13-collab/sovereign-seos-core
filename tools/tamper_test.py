#!/usr/bin/env python3
import json, argparse, sys, shutil, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import witness_sim as ws
import ast_check as ac

def main():
    p = argparse.ArgumentParser(); p.add_argument("--out", required=True); a = p.parse_args()
    src = Path(".")
    registry = {"witness-1", "witness-2", "witness-3"}
    cases = []
    def rec(name, expect_accept, got_accept, reason):
        cases.append({"case": name, "expected": "ACCEPT" if expect_accept else "REJECT",
                      "got": "ACCEPT" if got_accept else "REJECT",
                      "ok": expect_accept == got_accept, "reason": reason})
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "repo"
        root.mkdir()
        for d in ("tools", "policy"):
            if (src / d).is_dir():
                shutil.copytree(src / d, root / d, ignore=shutil.ignore_patterns("__pycache__"))
        for f in ("SKILL.md", "memory.yaml"):
            if (src / f).exists():
                shutil.copy(src / f, root / f)
        m = ws.build_manifest(root)
        if m is None:
            print("Tamper Test: FAIL (NO_EVIDENCE)"); sys.exit(1)
        sigs = [{"witness": w, "signature": ws.sign(m["digest"], w)} for w in sorted(registry)]
        ok, r = ws.verify_quorum(root, m["digest"], sigs, 2, registry)
        rec("T0 control: untouched artifacts", True, ok, r)
        victim = sorted((root / "tools").glob("*.py"))[0]
        victim.write_text(victim.read_text() + "\n# tampered\n")
        ok, r = ws.verify_quorum(root, m["digest"], sigs, 2, registry)
        rec("T1 file modified after signing", False, ok, r)
        shutil.copy(src / victim.relative_to(root), victim)
        forged = [sigs[0], {"witness": "witness-2", "signature": "00" * 32},
                  {"witness": "witness-3", "signature": "ff" * 32}]
        ok, r = ws.verify_quorum(root, m["digest"], forged, 2, registry)
        rec("T2 forged signatures", False, ok, r)
        dup = [sigs[0], sigs[0], {"witness": "evil", "signature": ws.sign(m["digest"], "evil")}]
        ok, r = ws.verify_quorum(root, m["digest"], dup, 2, registry)
        rec("T3 duplicate/unregistered witness", False, ok, r)
        empty = Path(td) / "empty"; empty.mkdir()
        ok, r = ws.verify_quorum(empty, m["digest"], sigs, 2, registry)
        rec("T4 missing evidence", False, ok, r)
        bad = Path(td) / "bad"; bad.mkdir(); (bad / "x.py").write_text("x = eval('1+1')\n")
        _, viol = ac.scan(bad)
        rec("T5 AST scanner on injected eval", False, not viol, f"{len(viol)} violation(s)")
        _, viol = ac.scan(empty)
        rec("T6 AST scanner on empty target", False, not viol, f"{len(viol)} violation(s)")
    status = "PASS" if all(c["ok"] for c in cases) else "FAIL"
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"status": status, "cases": cases}, indent=2))
    for c in cases:
        print(("ok  " if c["ok"] else "BAD ") + c["case"], "->", c["got"], "|", c["reason"])
    print("Tamper Test:", status)
    sys.exit(0 if status == "PASS" else 1)

if __name__ == "__main__":
    main()
