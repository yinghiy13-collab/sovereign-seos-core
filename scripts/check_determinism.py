import sys, json, re, argparse
from pathlib import Path
PATTERNS = [(r'\bMath\.random\s*\(', 'JS_RNG'), (r'^\s*(?:from\s+random\s+import|import\s+random\b)', 'PY_RNG_IMPORT'), (r'\brandom\.(random|randint|choice)\s*\(', 'PY_RNG_CALL'), (r'^\s*from\s+openai\s+import', 'LLM_IMPORT')]
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--scan', default='all'); ap.add_argument('--report', required=True); a = ap.parse_args()
    hits = []
    for root in ['skills', 'src', 'tools', 'scripts', 'index.html']:
        p = Path(root)
        if not p.exists(): continue
        files = [p] if p.is_file() else list(p.rglob('*'))
        for f in files:
            if not f.is_file() or 'check_determinism' in f.name: continue
            try: t = f.read_text()
            except: continue
            for pat, tag in PATTERNS:
                for m in re.finditer(pat, t, re.M): hits.append({'file':str(f),'tag':tag})
    Path(a.report).parent.mkdir(parents=True, exist_ok=True); Path(a.report).write_text(json.dumps({'hits':hits}))
    return 0 if not hits else 1
if __name__=='__main__': sys.exit(main())
