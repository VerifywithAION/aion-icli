param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Src = Join-Path $Repo "src\aion_self_patching_sandbox.py"
if (!(Test-Path $Src)) { throw "Missing source" }
& $Py -m py_compile $Src

$demoTarget = Join-Path $Repo "docs\DEMO_TARGET.md"
$existing = Test-Path $demoTarget
$beforeHash = ""
if ($existing) { $beforeHash = (Get-FileHash -Algorithm SHA256 $demoTarget).Hash }

$tempDir = Join-Path $Repo "release\_runtime\sandbox_verify_inputs"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Case {
  param([string]$Name,[hashtable]$Payload)
  $p = Join-Path $tempDir ("$Name.json")
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $p -Encoding UTF8
  $raw = & $Py $Src --input $p
  return ($raw | ConvertFrom-Json)
}

$safe = Invoke-Case -Name "safe" -Payload @{
  source="SelfRepairPlanner"; target_file="docs/DEMO_TARGET.md"; original_content="status: missing verifier"; proposed_content="status: verifier required before execution"; reason="demo"; verification_marker="AION_EXAMPLE_PATCH_OK"
}
if($safe.patch_status -ne "SANDBOXED_ONLY"){ throw "safe patch status mismatch" }
if($safe.production_mutation -ne "NOT_PERFORMED"){ throw "production mutation mismatch" }
if($safe.sandbox_mutation -ne "PERFORMED"){ throw "sandbox mutation mismatch" }
if($safe.rollback_available -ne $true){ throw "rollback false" }
if($safe.dry_run_verified -ne $true){ throw "dry-run false" }
if([string]::IsNullOrWhiteSpace($safe.hashes.original_sha256)){ throw "missing original hash" }
if([string]::IsNullOrWhiteSpace($safe.hashes.proposed_sha256)){ throw "missing proposed hash" }
if([string]::IsNullOrWhiteSpace($safe.hashes.rollback_sha256)){ throw "missing rollback hash" }
if($safe.hashes.original_sha256 -ne $safe.hashes.rollback_sha256){ throw "rollback hash mismatch" }
if(!(Test-Path (Join-Path $Repo $safe.receipt_path))){ throw "receipt path missing" }
if(!(Test-Path $safe.receipt_abs_path)){ throw "receipt abs missing" }
if($safe.receipt_written -ne $true){ throw "receipt_written false" }
if([string]::IsNullOrWhiteSpace($safe.receipt_sha256)){ throw "missing receipt sha" }

$abs = Invoke-Case -Name "abs" -Payload @{
  source="Manual"; target_file="C:\secret\file.txt"; original_content="a"; proposed_content="b"; reason="bad"; verification_marker="AION_EXAMPLE_PATCH_OK"
}
if($abs.patch_status -ne "REJECTED"){ throw "absolute path not rejected" }

$trav = Invoke-Case -Name "trav" -Payload @{
  source="Manual"; target_file="..\private\secret.txt"; original_content="a"; proposed_content="b"; reason="bad"; verification_marker="AION_EXAMPLE_PATCH_OK"
}
if($trav.patch_status -ne "REJECTED"){ throw "traversal not rejected" }

if(Test-Path $demoTarget){
  if(-not $existing){ throw "demo target was created in production" }
  $afterHash = (Get-FileHash -Algorithm SHA256 $demoTarget).Hash
  if($beforeHash -ne $afterHash){ throw "existing demo target hash changed" }
}

if(Test-Path (Join-Path $Repo "receipts\sandbox")) { Remove-Item -Path (Join-Path $Repo "receipts\sandbox") -Recurse -Force -ErrorAction SilentlyContinue }
if(Test-Path (Join-Path $Repo "release_runtime\sandbox")) { Remove-Item -Path (Join-Path $Repo "release_runtime\sandbox") -Recurse -Force -ErrorAction SilentlyContinue }
if(Test-Path $tempDir) { Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host "AION_SELF_PATCHING_SANDBOX_V1_VERIFY_OK"
