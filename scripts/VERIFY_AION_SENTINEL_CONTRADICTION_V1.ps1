param()

$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Target = Join-Path $Repo "src\aion_sentinel_contradiction.py"

if (!(Test-Path $Target)) { throw "Missing source: $Target" }
& $Py -m py_compile $Target

$tempDir = Join-Path $Repo "release\_runtime\sentinel_verify"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Scenario {
  param(
    [string]$Name,
    [hashtable]$Payload
  )
  $inputPath = Join-Path $tempDir ("{0}.json" -f $Name)
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $inputPath -Encoding UTF8
  $raw = & $Py $Target --input $inputPath
  return ($raw | ConvertFrom-Json)
}

$rA = Invoke-Scenario -Name "A" -Payload @{
  claim = "ready_to_ship"
  artifact = "scripts/deploy.ps1"
  evidence = @{ verifier = $false; receipt = $false; rollback = $false; dry_run = $false; human_review = $false }
  risk = @{ risk_level = "HIGH"; decision = "REVIEW_ONLY"; missing_controls = @("verifier", "rollback", "dry_run") }
  context = "ready to ship without proof"
}

$rB = Invoke-Scenario -Name "B" -Payload @{
  claim = "safe_to_execute"
  artifact = "scripts/run.ps1"
  evidence = @{ verifier = $true; receipt = $true; rollback = $true; dry_run = $true; human_review = $true }
  risk = @{ risk_level = "HIGH"; decision = "BLOCK"; missing_controls = @() }
  context = "safe to execute but blocked"
}

$rC = Invoke-Scenario -Name "C" -Payload @{
  claim = "allowed"
  artifact = "docs/policy.md"
  evidence = @{ verifier = $true; receipt = $true; rollback = $true; dry_run = $true; human_review = $true }
  risk = @{ risk_level = "LOW"; decision = "ALLOW"; missing_controls = @() }
  context = "aligned low risk"
}

if ($rA.consistency_status -ne "CONTRADICTION") { throw "Scenario A status expected CONTRADICTION" }
if ($rA.severity -ne "HIGH") { throw "Scenario A severity expected HIGH" }
if ($rA.governance_decision -ne "BLOCK") { throw "Scenario A decision expected BLOCK" }
if ($rC.consistency_status -ne "CONSISTENT") { throw "Scenario C status expected CONSISTENT" }
if ($rC.governance_decision -ne "ALLOW") { throw "Scenario C decision expected ALLOW" }

$results = @($rA, $rB, $rC)
foreach ($r in $results) {
  if ($r.boundary -ne "LOCAL_ONLY") { throw "boundary mismatch" }
  if ($r.network -ne "NOT_USED") { throw "network mismatch" }
  if ($r.mutation -ne "NOT_PERFORMED") { throw "mutation mismatch" }
  if ($r.execution -ne "NOT_PERFORMED") { throw "execution mismatch" }
  if ([string]::IsNullOrWhiteSpace($r.receipt_path)) { throw "missing receipt_path" }
  if ([string]::IsNullOrWhiteSpace($r.receipt_abs_path)) { throw "missing receipt_abs_path" }
  if ($r.receipt_written -ne $true) { throw "receipt_written must be true" }
  if ([string]::IsNullOrWhiteSpace($r.receipt_sha256)) { throw "missing receipt_sha256" }
  if (!(Test-Path (Join-Path $Repo $r.receipt_path))) { throw "receipt_path missing on disk" }
  if (!(Test-Path $r.receipt_abs_path)) { throw "receipt_abs_path missing on disk" }
}

$sentinelReceipts = Join-Path $Repo "receipts\sentinel"
if (Test-Path $sentinelReceipts) {
  Remove-Item -Path $sentinelReceipts -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "AION_SENTINEL_CONTRADICTION_V1_VERIFY_OK"
