param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Src = Join-Path $Repo "src\aion_self_patching_sandbox.py"
$tempDir = Join-Path $Repo "release\_runtime\sandbox_demo_inputs"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Case {
  param([string]$Name,[hashtable]$Payload)
  $p = Join-Path $tempDir ("$Name.json")
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $p -Encoding UTF8
  $raw = & $Py $Src --input $p
  return ($raw | ConvertFrom-Json)
}

$results = @()
$results += Invoke-Case -Name "safe_patch_proposal" -Payload @{
  source = "SelfRepairPlanner"
  target_file = "docs/DEMO_TARGET.md"
  original_content = "status: missing verifier"
  proposed_content = "status: verifier required before execution"
  reason = "repair missing control claim"
  verification_marker = "AION_EXAMPLE_PATCH_OK"
}
$results += Invoke-Case -Name "reject_absolute_path" -Payload @{
  source = "Manual"
  target_file = "C:\secret\file.txt"
  original_content = "a"
  proposed_content = "b"
  reason = "unsafe path"
  verification_marker = "AION_EXAMPLE_PATCH_OK"
}
$results += Invoke-Case -Name "reject_path_traversal" -Payload @{
  source = "Manual"
  target_file = "..\private\secret.txt"
  original_content = "a"
  proposed_content = "b"
  reason = "unsafe traversal"
  verification_marker = "AION_EXAMPLE_PATCH_OK"
}

$releasePath = Join-Path $Repo "release\AION_SELF_PATCHING_SANDBOX_V1_DEMO_RESULT.json"
$reportPath = Join-Path $Repo "reports\AION_SELF_PATCHING_SANDBOX_V1_DEMO_REPORT.md"
@{
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  sandbox = "AION_SELF_PATCHING_SANDBOX_V1"
  scenarios = $results
} | ConvertTo-Json -Depth 20 | Set-Content -Path $releasePath -Encoding UTF8

$lines = @(
  "# AION Self-Patching Sandbox V1 Demo Report",
  "",
  "Generated at UTC: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))",
  "",
  "## Scenario outcomes"
)
foreach($r in $results){
  $lines += "- target: $($r.target_file)"
  $lines += "  - status: $($r.patch_status)"
  $lines += "  - production_mutation: $($r.production_mutation)"
  $lines += "  - rollback_available: $($r.rollback_available)"
  $lines += "  - dry_run_verified: $($r.dry_run_verified)"
}
$lines += ""
$lines += "Marker: AION_SELF_PATCHING_SANDBOX_V1_DEMO_OK"
$lines -join "`r`n" | Set-Content -Path $reportPath -Encoding UTF8

Write-Host "AION_SELF_PATCHING_SANDBOX_V1_DEMO_OK"
