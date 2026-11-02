#!/usr/bin/env python3
"""L5 multi-sig witness using REAL Ed25519 cryptography (Simulation Mode)."""
import hashlib, json, argparse, sys
from pathlib import Path
from datetime import datetime, timezone
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("FATAL: pip install cryptography"); sys.exit(1)

def build_manifest(root: Path):
    files = sorted(p for pat in ("tools/*.py", "policy/*.rego", "SKILL.md", "memory.yaml")
                   for p in root.glob(pat))
    if not files:
        return None
    entries = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    digest = hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()
    return {"files": entries, "digest": "sha256:" + digest}

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
        
    # 1. สร้าง Keypair (จำลองสำหรับ CI)
    # ในระบบจริง Private Key ต้องอยู่ใน GitHub Secrets และ Public Key อยู่ใน Registry
    private_keys = [ed25519.Ed25519PrivateKey.generate() for _ in range(a.n)]
    public_keys = [pk.public_key() for pk in private_keys]
    
    registry = {}
    sigs = []
    
    # 2. ลงนาม
    payload = m["digest"].encode('utf-8')
    for i, pk in enumerate(private_keys):
        wid = f"witness-{i+1}"
        # เก็บ Public Key ลง registry (แปลงเป็น Hex)
        pub_bytes = public_keys[i].public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        registry[wid] = pub_bytes.hex()
        
        # เซ็นด้วย Private Key
        sig = pk.sign(payload)
        sigs.append({"witness": wid, "signature": sig.hex()})
        
    # 3. ตรวจสอบ Quorum (Verification)
    valid_sigs = set()
    for s in sigs:
        wid = s["witness"]
        if wid in registry:
            try:
                pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(registry[wid]))
                pub_key.verify(bytes.fromhex(s["signature"]), payload)
                valid_sigs.add(wid)
            except Exception:
                pass # ลายเซ็นไม่ถูกต้อง
                
    ok = len(valid_sigs) >= a.k
    reason = f"OK: {len(valid_sigs)}/{a.k} valid" if ok else f"QUORUM_NOT_MET: {len(valid_sigs)}/{a.k} valid"
    
    rep = {
        "status": "PASS" if ok else "FAIL",
        "reason": reason,
        "k": a.k, "n": a.n,
        "algorithm": "Ed25519",
        "manifest_digest": m["digest"],
        "registry": registry,
        "signatures": sigs,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=2))
    print(f"Witness Ed25519: {rep['status']} ({reason})")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
