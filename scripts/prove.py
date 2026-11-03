import sys, json, hashlib, datetime
from pathlib import Path
rows, ok_all = [], True
for c in ['C1','C2','C3','C4','C5','C6','C7']:
    f = Path(f'artifacts/{c.lower()}.json')
    if not f.exists(): rows.append({'check':c,'status':'MISSING'}); ok_all=False; continue
    d = json.loads(f.read_text()); fail = d.get('fails',0) or d.get('violations') or d.get('broken') or d.get('hits') or d.get('deleted') or []
    ok = not fail; rows.append({'check':c,'status':'PASS' if ok else 'FAIL','evidence_digest':hashlib.sha256(f.read_bytes()).hexdigest()[:16]}); ok_all &= ok
root = hashlib.sha256(json.dumps([r['evidence_digest'] for r in rows], sort_keys=True).encode()).hexdigest()

# เพิ่ม layer และ status ตรงนี้
rep = {
    'layer': 'L7',
    'decision': 'ALLOW' if ok_all else 'DENY',
    'status': 'PASS' if ok_all else 'FAIL',
    'checks': rows,
    'evidence_root': root
}

Path('proof').mkdir(exist_ok=True); Path('proof/report.json').write_text(json.dumps(rep, indent=2))
print('='*50); [print(f"  {r['check']}  {r['status']}  {r.get('evidence_digest','-')}") for r in rows]; print('='*50); print(f"  DECISION : {rep['decision']}\n  evidence_root: {root[:32]}...")
sys.exit(0 if ok_all else 1)
