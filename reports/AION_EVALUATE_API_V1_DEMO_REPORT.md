# AION Evaluate API V1 Demo Report

- Endpoint: `http://127.0.0.1:8765/evaluate`
- Generated UTC: 2026-05-11T19:23:53Z

| Scenario | Expected | Actual | Risk | Receipt | SHA256 |
|---|---|---|---|---|---|
| flagged_block | BLOCK | BLOCK | HIGH | receipts/evaluate/20260511T192353Z_aion_eval_8d5195f271f0.json | e9e419d849ff4ee8787de482c4c54f98d3d0a1544da7df732d6b5491199d8c81 |
| watch_warn | WARN | WARN | MEDIUM | receipts/evaluate/20260511T192353Z_aion_eval_dafbd29db362.json | 4b70ea66a6e178f654e06acd55037bf260c3bb7b30974b3395ec206d48c7bff0 |
| clean_allow | ALLOW | ALLOW | LOW | receipts/evaluate/20260511T192353Z_aion_eval_1d206a1594f0.json | 54f7680b9a6cde5f61eb909d34d8a7788bd1c33f0ccca80fd41425aebaf6a8c7 |
