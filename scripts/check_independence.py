import sys, json, re, yaml, argparse
from pathlib import Path
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--max-tools', type=int, default=2); ap.add_argument('--report', required=True); a = ap.parse_args()
    files = sorted(Path('skills').glob('*.md')); v = []
    for p in files:
        m = re.match(r'^---\s*\n(.*?)\n---\s*\n', p.read_text(), re.S)
        if not m: continue
        meta = yaml.safe_load(m.group(1))
        instr = str(meta.get('instructions', ''))
        for step in re.split(r'\n(?=\s*step_id:)', instr):
            if len(re.findall(r'^\s*tool:', step, re.M)) > a.max_tools: v.append({'file':p.name})
    Path(a.report).parent.mkdir(parents=True, exist_ok=True); Path(a.report).write_text(json.dumps({'violations':v}))
    return 0 if not v else 1
if __name__=='__main__': sys.exit(main())
