# Public Demo Release Pack V1

Public demo release artifact for rapid reviewer/investor/developer inspection.

## Package

- ZIP: `dist\aion-public-demo-release-pack-v1.zip`
- SHA256: `54FFBD4E701820BEAC261D0043FA67705F90C79EF48AC115B81174535BC7009B`
- Source head: `a4117e6`

## Included

- README public demo section
- Agent Claim vs AION Proof Gate docs/reports
- Fresh-clone acceptance docs/report
- Demo claims/artifacts/output folder
- Demo run/verify scripts
- CLI entrypoint and launchers

## Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_DEMO_RELEASE_PACK_V1.ps1
```

Expected marker:

- `AION_PUBLIC_DEMO_RELEASE_PACK_V1_VERIFY_OK`

## Public-safe boundary

- local/offline workflow
- no provider/API calls
- no execution of user artifacts
- no mutation claims
