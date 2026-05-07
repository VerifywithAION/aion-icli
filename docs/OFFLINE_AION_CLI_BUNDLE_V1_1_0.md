# OFFLINE AION CLI BUNDLE V1.1.0

AION ICLI Offline Bundle V1.1.0 packages the current public-safe intelligence layers from main.

- Source head commit: 5532ae2
- Package name: aion-icli-offline-bundle-v1.1.0.zip
- Package path: dist/aion-icli-offline-bundle-v1.1.0.zip
- SHA256: 66295913932adc0a8b067ad13204263262674275dd9ec92989febfa213ee9536

## Included layers

- Artifact Inspection Runner V1
- Memory Scar Engine V1
- Living Proof Graph V1
- Evidence Engine V1
- Introspection Gate V1
- Contradiction Engine V1
- Self-Repair Planner V1
- Sentinel Consistency Engine V1

## Public-safe exclusions

- .git
- receipts/local
- runtime local receipts
- node_modules
- __pycache__
- .venv / venv
- .env
- secrets/private paths

## Install

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
.\bin\aion.cmd "Who are you, AION?"
.\bin\aion.cmd "sentinel state"
```

## Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_OFFLINE_AION_CLI_BUNDLE_V1_1_0.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_OFFLINE_AION_CLI_BUNDLE_V1_1_0_FRESH_INSTALL.ps1
```

## Caveat

`v1.0.0-public-icli` remains historical. `v1.1.0-offline-icli` carries current main intelligence layers.
