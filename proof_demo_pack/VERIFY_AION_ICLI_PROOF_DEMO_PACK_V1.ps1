param()

$ErrorActionPreference = "Stop"

$packRoot = $PSScriptRoot

$required = @(
    (Join-Path $packRoot "AION_ICLI_PROOF_DEMO_PACK_V1.json"),
    (Join-Path $packRoot "reports\AION_ICLI_PROOF_DEMO_PACK_V1_REPORT.md"),
    (Join-Path $packRoot "SCREENSHOT_CHECKLIST.md")
)

foreach ($path in $required) {

    if (!(Test-Path $path)) {
        throw "Missing required proof pack artifact: $path"
    }
}

Write-Host ""
Write-Host "AION_ICLI_PROOF_DEMO_PACK_V1_VERIFY_OK"
Write-Host ""
