# AION ICLI GitHub Release V1 Checklist

## Release

- Title: AION ICLI Public Release V1 — Governed Command Line Intelligence
- Tag: v1.0.0-public-icli
- Target commit: 2fea528
- Asset: dist/aion-icli-public-install-package-v1.zip
- SHA256: 8B99C3C7161F2911212E7D57A4F3A3782700DBBCE404288D1E4AD6A671D7D746

## Before publishing

- [ ] Confirm repo head is `2fea528`
- [ ] Confirm ZIP SHA256 matches expected hash
- [ ] Confirm `docs/USER_GUIDE_V1.md` exists
- [ ] Confirm `scripts/VERIFY_USER_GUIDE_V1.ps1` exists
- [ ] Confirm `docs/GITHUB_RELEASE_V1_DRAFT.md` exists
- [ ] Confirm no private credentials are present
- [ ] Confirm no `.env`, `.codara`, `.aion`, `node_modules`, `private`, or `secrets` folders are included
- [ ] Confirm release body uses public-safe wording
- [ ] Attach ZIP asset to GitHub Release
- [ ] Copy SHA256 into release body

## Verification commands

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_CONNECTOR_POLICY_V2.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_USER_GUIDE_V1.ps1

## Expected markers

    AION_ICLI_PUBLIC_SAFE_VERIFY_OK
    AION_CONNECTOR_POLICY_V2_VERIFY_OK
    AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK
    AION_USER_GUIDE_V1_VERIFY_OK

## Status

LOCKED as AION ICLI GitHub Release V1 Checklist.
