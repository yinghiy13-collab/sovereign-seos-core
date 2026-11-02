import sys, json, yaml, re, argparse
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--threshold', type=float, default=0.85); ap.add_argument('--report', required=True); a = ap.parse_args()
    files = sorted(Path('skills').glob('*.md'))
    if len(files) < 2: Path(a.report).write_text(json.dumps({'violations':[]})); return 0
    docs = [p.read_text() for p in files]
    X = TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True).fit_transform(docs)
    S = cosine_similarity(X); v = []
    for i in range(len(files)):
        for j in range(i+1, len(files)):
            if S[i,j] >= a.threshold: v.append({'a':files[i].name,'b':files[j].name,'sim':float(S[i,j])})
    Path(a.report).parent.mkdir(parents=True, exist_ok=True); Path(a.report).write_text(json.dumps({'violations':v}))
    return 0 if not v else 1
if __name__=='__main__': sys.exit(main())
