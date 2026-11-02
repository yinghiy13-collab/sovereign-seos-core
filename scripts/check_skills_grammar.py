import sys, re, json, yaml, argparse
from pathlib import Path
FM = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.S)
REQ = {'skill_id','version','status','description','tools'}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--strict', action='store_true'); ap.add_argument('--report', required=True); a = ap.parse_args()
    files = sorted(Path('skills').glob('*.md')); rep, fails = [], 0
    if not files: print('FAIL: no skills'); return 1
    for p in files:
        m = FM.match(p.read_text())
        if not m: fails+=1; rep.append({'file':str(p),'pass':False}); continue
        meta = yaml.safe_load(m.group(1))
        ok = not (REQ - set(meta))
        if not ok: fails+=1
        rep.append({'file':str(p),'pass':ok})
        print(f'{"PASS" if ok else "FAIL"}: {p.name}')
    Path(a.report).parent.mkdir(parents=True, exist_ok=True); Path(a.report).write_text(json.dumps({'fails':fails}))
    return 0 if fails==0 else 1
if __name__=='__main__': sys.exit(main())
