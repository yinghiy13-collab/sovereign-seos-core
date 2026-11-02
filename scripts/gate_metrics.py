import sys, json, math, argparse
from pathlib import Path
def wilson(p, n, z):
    if n == 0: return 0.0
    z2 = z*z; return (p + z2/(2*n) - z*math.sqrt(p*(1-p)/n + z2/(4*n*n)))/(1 + z2/n)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--n-min', type=int, default=30); ap.add_argument('--z', type=float, default=1.645); ap.add_argument('--report', required=True); a = ap.parse_args()
    f = Path('evidence/metrics.json')
    if not f.exists(): Path(a.report).write_text(json.dumps({'fails':0})); return 0
    m = json.loads(f.read_text()); fails = 0
    for s in m.get('skills', []):
        n = s.get('n_trials',0); p = s.get('errors',0)/n if n else 0; pb = s.get('baseline_error_rate', 0.1)
        if n >= a.n_min and wilson(p, n, a.z) > 1.1 * pb: fails += 1
    Path(a.report).parent.mkdir(parents=True, exist_ok=True); Path(a.report).write_text(json.dumps({'fails':fails}))
    return 0 if fails == 0 else 1
if __name__=='__main__': sys.exit(main())
