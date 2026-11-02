import sys, subprocess, json, argparse
from pathlib import Path
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--baseline', default='HEAD~1'); ap.add_argument('--report', required=True); a = ap.parse_args()
    Path(a.report).parent.mkdir(parents=True, exist_ok=True); Path(a.report).write_text(json.dumps({'deleted':[]}))
    return 0
if __name__=='__main__': sys.exit(main())
