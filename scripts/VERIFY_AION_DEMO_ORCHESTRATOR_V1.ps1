param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$src = Join-Path $Repo "src\aion_demo_orchestrator.py"

if (!(Test-Path $src)) { throw "Missing source" }
& $Py -m py_compile $src

$raw = & $Py $src run
$result = $raw | ConvertFrom-Json

if ($result.final_demo_verdict -ne "PASS") { throw "final_demo_verdict must be PASS" }
foreach($s in $result.steps){ if($s.status -ne "PASS"){ throw "Step not PASS: $($s.step)" } }

$map = @{}
foreach($s in $result.steps){ $map[$s.step] = $s }

if($map['preflight'].actual -ne 'BLOCK'){ throw 'preflight actual must BLOCK' }
if($map['memory'].actual -ne 'BLOCK'){ throw 'memory bias must BLOCK' }
if($map['sentinel'].actual -ne 'CONTRADICTION'){ throw 'sentinel must CONTRADICTION' }
if($map['self_repair'].actual -ne 'PLAN_ONLY'){ throw 'self_repair must PLAN_ONLY' }
if($map['sandbox'].actual -ne 'SANDBOXED_ONLY'){ throw 'sandbox must SANDBOXED_ONLY' }
if($map['sandbox'].summary.production_mutation -ne 'NOT_PERFORMED'){ throw 'sandbox production mutation must NOT_PERFORMED' }
if($map['sandbox'].summary.rollback_available -ne $true){ throw 'sandbox rollback must true' }
if($map['domain_governor'].actual -ne 'BLOCK'){ throw 'domain governor must BLOCK' }
if($map['intuition'].actual -ne 'CRITICAL_SIGNAL'){ throw 'intuition must CRITICAL_SIGNAL' }
if($map['introspection'].actual -ne 'GRAPH_WRITTEN'){ throw 'introspection graph not written' }

if($result.public_safe -ne $true){ throw 'public_safe must true' }
if($result.boundary -ne 'LOCAL_ONLY'){ throw 'boundary mismatch' }
if($result.network -ne 'NOT_USED'){ throw 'network mismatch' }
if($result.execution -ne 'GOVERNED_ACTION_NOT_EXECUTED'){ throw 'execution mismatch' }
if([string]::IsNullOrWhiteSpace($result.receipt_path)){ throw 'receipt_path missing' }
if([string]::IsNullOrWhiteSpace($result.receipt_abs_path)){ throw 'receipt_abs_path missing' }
if($result.receipt_written -ne $true){ throw 'receipt_written false' }
if([string]::IsNullOrWhiteSpace($result.receipt_sha256)){ throw 'receipt_sha256 missing' }
if(!(Test-Path (Join-Path $Repo $result.receipt_path))){ throw 'receipt_path file missing' }
if(!(Test-Path $result.receipt_abs_path)){ throw 'receipt_abs file missing' }

$cleanup = @(
  'receipts\demo_orchestrator',
  'receipts\preflight',
  'receipts\memory',
  'receipts\sentinel',
  'receipts\self_repair',
  'receipts\sandbox',
  'receipts\domain_governors',
  'receipts\intuition',
  'receipts\introspection',
  'release_runtime\sandbox'
)
foreach($c in $cleanup){
  $p = Join-Path $Repo $c
  if(Test-Path $p){ Remove-Item -Path $p -Recurse -Force -ErrorAction SilentlyContinue }
}

Write-Host "AION_DEMO_ORCHESTRATOR_V1_VERIFY_OK"
