param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Src = Join-Path $Repo "src\aion_creativity_intuition.py"
if(!(Test-Path $Src)){ throw "Missing source" }
& $Py -m py_compile $Src

$tempDir = Join-Path $Repo "release\_runtime\intuition_verify_inputs"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Case {
  param([string]$Name,[hashtable]$Payload)
  $p = Join-Path $tempDir ("$Name.json")
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $p -Encoding UTF8
  $raw = & $Py $Src --input $p
  return ($raw | ConvertFrom-Json)
}

$a = Invoke-Case -Name "wallet" -Payload @{ source="DomainGovernor"; context="wallet"; signals=@{ contradictions=1; memory_matches=2; missing_controls=@("verifier","rollback"); risk_signals=@("signature","funds_at_risk"); domain="wallet"; governance_decision="BLOCK"; evidence_complete=$false; proof_graph_missing_count=0 } }
$b = Invoke-Case -Name "agent" -Payload @{ source="Sentinel"; context="agent"; signals=@{ contradictions=1; memory_matches=1; missing_controls=@("verifier"); risk_signals=@("unsafe_claim"); domain="agent"; governance_decision="REVIEW_ONLY"; evidence_complete=$false; proof_graph_missing_count=0 } }
$c = Invoke-Case -Name "clean" -Payload @{ source="Manual"; context="clean"; signals=@{ contradictions=0; memory_matches=0; missing_controls=@(); risk_signals=@(); domain="unknown"; governance_decision="ALLOW"; evidence_complete=$true; proof_graph_missing_count=0 } }

if($a.intuition_class -ne "CRITICAL_SIGNAL"){ throw "wallet case must be CRITICAL_SIGNAL" }
if($c.intuition_class -ne "LOW_SIGNAL"){ throw "clean case must be LOW_SIGNAL" }

foreach($r in @($a,$b,$c)){
  if($r.heuristic_not_truth -ne $true){ throw "heuristic_not_truth false" }
  if($r.forbidden_actions -notcontains "do_not_treat_intuition_as_proof"){ throw "missing forbidden action" }
  if($r.boundary -ne "LOCAL_ONLY"){ throw "boundary mismatch" }
  if($r.network -ne "NOT_USED"){ throw "network mismatch" }
  if($r.mutation -ne "NOT_PERFORMED"){ throw "mutation mismatch" }
  if($r.execution -ne "NOT_PERFORMED"){ throw "execution mismatch" }
  if([string]::IsNullOrWhiteSpace($r.receipt_path)){ throw "receipt_path missing" }
  if([string]::IsNullOrWhiteSpace($r.receipt_abs_path)){ throw "receipt_abs_path missing" }
  if($r.receipt_written -ne $true){ throw "receipt_written false" }
  if([string]::IsNullOrWhiteSpace($r.receipt_sha256)){ throw "receipt_sha256 missing" }
  if(!(Test-Path (Join-Path $Repo $r.receipt_path))){ throw "receipt_path file missing" }
  if(!(Test-Path $r.receipt_abs_path)){ throw "receipt_abs file missing" }
  foreach($act in $r.creative_next_actions){
    $allText = (($act.title.ToString() + " " + $act.why.ToString()).ToLower())
    if($allText -match "\bexecute\b|run now|apply now"){ throw "creative action suggests execution" }
  }
}

if(Test-Path (Join-Path $Repo "receipts\intuition")){ Remove-Item -Path (Join-Path $Repo "receipts\intuition") -Recurse -Force -ErrorAction SilentlyContinue }
if(Test-Path $tempDir){ Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host "AION_CREATIVITY_INTUITION_V1_VERIFY_OK"
