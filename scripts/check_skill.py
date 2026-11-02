import sys, re, yaml
from pathlib import Path
if __name__ == '__main__':
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', Path(sys.argv[1]).read_text(), re.S)
    sys.exit(0 if m and yaml.safe_load(m.group(1)).get('skill_id') else 1)
