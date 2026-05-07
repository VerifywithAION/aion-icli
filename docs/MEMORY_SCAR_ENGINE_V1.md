# AION Memory Scar Engine V1

Expected marker: `AION_MEMORY_SCAR_ENGINE_V1_VERIFY_OK`

AION is not storing chat memories. AION stores behavior-changing scars.

Each memory scar captures:
- trigger
- harm
- repair
- future_rule

This is the seed of non-token learning: store failure patterns, retrieve rules, apply governance before action.

Memory note vs memory scar:
- note: passive observation
- scar: enforced future rule after proven harm

Public-safe runtime paths:
- `.aion_public/scars/scars_seed.jsonl`
- `.aion_public/graph/proof_graph_seed.json`
- `.aion_public/evolution/evolution_ledger_seed.jsonl`

This is local governance memory only:
- no network
- no provider calls
- no autonomous execution
- no canonical mutation execution
