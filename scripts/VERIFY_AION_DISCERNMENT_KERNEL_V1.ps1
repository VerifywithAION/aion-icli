param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

if (!(Test-Path .\src\aion_discernment_kernel.py)) { throw "Missing discernment source" }
python -m py_compile .\src\aion_discernment_kernel.py

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_DISCERNMENT_KERNEL_V1_DEMO.ps1 | Out-Null

$data = Get-Content -Raw -Path .\release\AION_DISCERNMENT_KERNEL_V1_DEMO_RESULT.json | ConvertFrom-Json
if (-not $data.results) { throw "Missing demo results" }

$map = @{}
foreach ($r in $data.results) { $map[$r.scenario] = $r.result }

foreach ($name in @("trading","home_robot","shopping","coding","mirror")) {
  if (-not $map.ContainsKey($name)) { throw "Missing scenario: $name" }
  $res = $map[$name]
  if ($res.engine -ne "AION_DISCERNMENT_KERNEL_V1") { throw "Engine mismatch for $name" }
  if ([string]::IsNullOrWhiteSpace($res.one_question_that_matters)) { throw "Missing one_question_that_matters for $name" }
  if ([string]::IsNullOrWhiteSpace($res.safe_next_step)) { throw "Missing safe_next_step for $name" }
  if ($res.boundary -ne "LOCAL_ONLY") { throw "Boundary mismatch for $name" }
  if ($res.network -ne "NOT_USED") { throw "Network mismatch for $name" }
  if ($res.mutation -ne "NOT_PERFORMED") { throw "Mutation mismatch for $name" }
  if ($res.execution -ne "NOT_PERFORMED") { throw "Execution mismatch for $name" }
  if (-not $res.receipt_written) { throw "receipt_written false for $name" }
  if (-not (Test-Path $res.receipt_abs_path)) { throw "receipt_abs_path missing for $name" }
}

if ($map["trading"].discernment_verdict -ne "ASK_HUMAN_FIRST") { throw "Trading verdict should be ASK_HUMAN_FIRST" }
if ($map["home_robot"].discernment_verdict -ne "ASK_HUMAN_FIRST") { throw "Home robot verdict should be ASK_HUMAN_FIRST" }
if ($map["shopping"].discernment_verdict -ne "ASK_HUMAN_FIRST") { throw "Shopping verdict should be ASK_HUMAN_FIRST" }
if ($map["coding"].discernment_verdict -ne "HARD_STOP") { throw "Coding verdict should be HARD_STOP" }

Write-Host "AION_DISCERNMENT_KERNEL_V1_VERIFY_OK"
