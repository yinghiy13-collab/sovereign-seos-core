.PHONY: prove c1 c2 c3 c4 c5 c6 c7 clean
c1: ; @python scripts/check_skills_grammar.py --strict --report artifacts/c1.json || true
c2: ; @python scripts/check_deduplication.py --threshold 0.85 --report artifacts/c2.json || true
c3: ; @python scripts/gate_metrics.py --n-min 30 --z 1.645 --report artifacts/c3.json || true
c4: ; @python scripts/check_independence.py --max-tools 2 --report artifacts/c4.json || true
c5: ; @python scripts/check_no_delete.py --baseline HEAD --report artifacts/c5.json || true
c6: ; @python scripts/check_determinism.py --scan all --report artifacts/c6.json || true
c7: ; @python scripts/verify_ledger.py --report artifacts/c7.json || true
prove: c1 c2 c3 c4 c5 c6 c7 ; @python scripts/prove.py
clean: ; @rm -f artifacts/*.json proof/*.json
