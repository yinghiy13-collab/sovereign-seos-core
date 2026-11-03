import json, sys, argparse
from pathlib import Path
try:
    import jsonschema
except ImportError:
    print("Please install jsonschema: pip install jsonschema")
    sys.exit(1)

def validate(filepath, schema_path):
    try:
        schema = json.loads(Path(schema_path).read_text())
        data = json.loads(Path(filepath).read_text())
        jsonschema.validate(instance=data, schema=schema)
        
        # Fail-Closed Logic Check
        if data.get('decision') == 'ALLOW' and data.get('status') == 'NOT_RUN':
            print(f"❌ FAIL: Cannot ALLOW when status is NOT_RUN ({filepath})")
            return False
        print(f"✅ PASS: {filepath} is valid.")
        return True
    except Exception as e:
        print(f"❌ FAIL: {filepath} - {e}")
        return False

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--file', required=True)
    ap.add_argument('--layer', required=True)
    args = ap.parse_args()
    sys.exit(0 if validate(args.file, 'schemas/evidence_layer.schema.json') else 1)
