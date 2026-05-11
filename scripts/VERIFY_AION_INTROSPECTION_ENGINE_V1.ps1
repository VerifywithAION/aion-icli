param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Src = Join-Path $Repo "src\aion_introspection_engine.py"

if (!(Test-Path $Src)) { throw "Missing source: $Src" }
& $Py -m py_compile $Src

$raw = & $Py $Src build
$result = $raw | ConvertFrom-Json

$jsonPath = Join-Path $Repo "release\AION_LIVING_PROOF_GRAPH_V1.json"
$mdPath = Join-Path $Repo "reports\AION_LIVING_PROOF_GRAPH_V1.md"
if (!(Test-Path $jsonPath)) { throw "Missing $jsonPath" }
if (!(Test-Path $mdPath)) { throw "Missing $mdPath" }

$graph = Get-Content -Raw -Path $jsonPath | ConvertFrom-Json
if ($graph.engine -ne "AION_INTROSPECTION_ENGINE_V1") { throw "Engine mismatch" }

$names = @($graph.proven_capabilities | ForEach-Object { $_.name })
foreach($need in @("Evaluate API Adapter V1","Preflight Gate V1","Memory Scars V1","Sentinel + Contradiction Engine V1")){
  if($names -notcontains $need){ throw "Missing capability: $need" }
}

$markers = @($graph.core_locked_markers)
foreach($m in @("AION_EVALUATE_API_V1_VERIFY_OK","AION_PREFLIGHT_GATE_V1_VERIFY_OK","AION_MEMORY_SCARS_V1_VERIFY_OK","AION_SENTINEL_CONTRADICTION_V1_VERIFY_OK")){
  if($markers -notcontains $m){ throw "Missing locked marker: $m" }
}

if ([string]::IsNullOrWhiteSpace($graph.next_build_pointer)) { throw "Missing next_build_pointer" }

if ([string]::IsNullOrWhiteSpace($result.receipt_path)) { throw "Missing receipt_path" }
if ([string]::IsNullOrWhiteSpace($result.receipt_abs_path)) { throw "Missing receipt_abs_path" }
if ($result.receipt_written -ne $true) { throw "receipt_written must be true" }
if ([string]::IsNullOrWhiteSpace($result.receipt_sha256)) { throw "Missing receipt_sha256" }
if (!(Test-Path (Join-Path $Repo $result.receipt_path))) { throw "receipt_path not found" }
if (!(Test-Path $result.receipt_abs_path)) { throw "receipt_abs_path not found" }

$receiptDir = Join-Path $Repo "receipts\introspection"
if (Test-Path $receiptDir) {
  Remove-Item -Path $receiptDir -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "AION_INTROSPECTION_ENGINE_V1_VERIFY_OK"
