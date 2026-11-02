#!/usr/bin/env python3
import hashlib, hmac, json, argparse, sys
from pathlib import Path
from datetime import datetime, timezone

def build_manifest(root: Path):
    files = sorted(p for pat in ("tools/*.py", "policy/*.rego", "SKILL.md", "memory.yaml")
                   for p in root.glob(pat))
    if not files:
        return None
    entries = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    digest = hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()
    return {"files": entries, "digest": "sha256:" + digest}

def _key(wid: str) -> bytes:
    return hashlib.sha256(b"seos-sim-witness-" + wid.encode()).digest()

def sign(digest: str, wid: str) -> str:
    return hmac.new(_key(wid), digest.encode(), hashlib.sha256).hexdigest()

def verify_quorum(root: Path, signed_digest: str, sigs: list, k: int, registry: set):
    m = build_manifest(root)
    if m is None:
        return False, "NO_EVIDENCE: no files to build manifest"
    if m["digest"] != signed_digest:
        return False, "DIGEST_MISMATCH: artifacts changed after signing"
    valid = set()
    for s in sigs:
        w = s.get("witness")
        if w in registry and hmac.compare_digest(s.get("signature", ""), sign(m["digest"], w)):
            valid.add(w)
    if len(valid) < k:
        return False, f"QUORUM_NOT_MET: {len(valid)}/{k} valid"
    return True, f"OK: {len(valid)}/{k} valid"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--k", type=int, required=True)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    root = Path(".")
    m = build_manifest(root)
    if m is None:
        print("Witness Sim: FAIL (NO_EVIDENCE)"); sys.exit(1)
    Path("evidence_manifest.json").write_text(json.dumps(m, indent=2))
    registry = {f"witness-{i+1}" for i in range(a.n)}
    sigs = [{"witness": w, "signature": sign(m["digest"], w)} for w in sorted(registry)]
    ok, reason = verify_quorum(root, m["digest"], sigs, a.k, registry)
    rep = {"status": "PASS" if ok else "FAIL", "reason": reason, "k": a.k, "n": a.n,
           "manifest_digest": m["digest"], "signatures": sigs, "simulation": True,
           "timestamp": datetime.now(timezone.utc).isoformat()}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=2))
    print(f"Witness Sim: {rep['status']} ({reason})")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
