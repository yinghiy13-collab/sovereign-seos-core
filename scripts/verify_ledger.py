import sys, json, hashlib, argparse
from pathlib import Path
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--report', required=True); a = ap.parse_args()
    p = Path('evidence/ledger.jsonl')
    if not p.exists(): Path(a.report).write_text(json.dumps({'broken':[]})); return 0
    prev = '0'*64; broken = []
    for i, line in enumerate(p.read_text().splitlines()):
        if not line.strip(): continue
        e = json.loads(line); dg = hashlib.sha256(json.dumps(e['payload'], sort_keys=True).encode()).hexdigest()
        if e.get('prev') != prev or e.get('digest') != dg: broken.append({'i':i})
        prev = dg
    Path(a.report).parent.mkdir(parents=True, exist_ok=True); Path(a.report).write_text(json.dumps({'broken':broken}))
    return 0 if not broken else 1
if __name__=='__main__': sys.exit(main())
