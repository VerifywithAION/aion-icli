param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Src = Join-Path $Repo "src\aion_domain_governors.py"
if (!(Test-Path $Src)) { throw "Missing source" }
& $Py -m py_compile $Src

$tempDir = Join-Path $Repo "release\_runtime\domain_verify_inputs"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Case {
  param([string]$Name,[hashtable]$Payload)
  $p = Join-Path $tempDir ("$Name.json")
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $p -Encoding UTF8
  $raw = & $Py $Src --input $p
  return ($raw | ConvertFrom-Json)
}

function Ctl([bool]$v,[bool]$r,[bool]$rb,[bool]$d,[bool]$h){ return @{ verifier=$v; receipt=$r; rollback=$rb; dry_run=$d; human_review=$h } }

$cases = @(
  @{name="agent"; expect="BLOCK"; payload=@{domain="agent";source="Agent";action="exec";risk_level="HIGH";signals=@("execution","unsafe_claim");controls=(Ctl $false $true $false $true $false);requested_execution=$true}},
  @{name="wallet"; expect="BLOCK"; payload=@{domain="wallet";source="WalletGuard";action="sign";risk_level="HIGH";signals=@("signature","funds_at_risk");controls=(Ctl $true $true $true $true $false);requested_execution=$false}},
  @{name="security"; expect="BLOCK"; payload=@{domain="security";source="BuzzShield";action="flagged";risk_level="HIGH";signals=@("flagged","exploit");controls=(Ctl $true $true $true $true $true);requested_execution=$false}},
  @{name="trading"; expect="BLOCK"; payload=@{domain="trading";source="Manual";action="trade";risk_level="MEDIUM";signals=@("execution");controls=(Ctl $true $true $true $false $true);requested_execution=$true}},
  @{name="quantum"; expect="BLOCK"; payload=@{domain="quantum";source="AION";action="quantum";risk_level="MEDIUM";signals=@("execution");controls=(Ctl $false $true $true $true $true);requested_execution=$true}},
  @{name="physical_ai"; expect="BLOCK"; payload=@{domain="physical_ai";source="Manual";action="actuate";risk_level="HIGH";signals=@("execution");controls=(Ctl $true $true $true $true $false);requested_execution=$true}},
  @{name="unknown"; expect="REVIEW_ONLY"; payload=@{domain="unknown";source="Manual";action="unknown";risk_level="UNKNOWN";signals=@();controls=(Ctl $true $true $true $true $true);requested_execution=$false}}
)

foreach($c in $cases){
  $r = Invoke-Case -Name $c.name -Payload $c.payload
  if($r.engine -ne "AION_DOMAIN_GOVERNORS_V1"){ throw "engine mismatch for $($c.name)" }
  if([string]::IsNullOrWhiteSpace($r.selected_governor)){ throw "selected governor missing $($c.name)" }
  if($r.governance_decision -ne $c.expect){ throw "decision mismatch for $($c.name): expected $($c.expect) got $($r.governance_decision)" }
  if($r.boundary -ne "LOCAL_ONLY"){ throw "boundary mismatch $($c.name)" }
  if($r.network -ne "NOT_USED"){ throw "network mismatch $($c.name)" }
  if($r.mutation -ne "NOT_PERFORMED"){ throw "mutation mismatch $($c.name)" }
  if($r.execution -ne "NOT_PERFORMED"){ throw "execution mismatch $($c.name)" }
  if([string]::IsNullOrWhiteSpace($r.receipt_path)){ throw "receipt_path missing $($c.name)" }
  if([string]::IsNullOrWhiteSpace($r.receipt_abs_path)){ throw "receipt_abs_path missing $($c.name)" }
  if($r.receipt_written -ne $true){ throw "receipt_written false $($c.name)" }
  if([string]::IsNullOrWhiteSpace($r.receipt_sha256)){ throw "receipt_sha missing $($c.name)" }
  if(!(Test-Path (Join-Path $Repo $r.receipt_path))){ throw "receipt path file missing $($c.name)" }
  if(!(Test-Path $r.receipt_abs_path)){ throw "receipt abs file missing $($c.name)" }
}

if(Test-Path (Join-Path $Repo "receipts\domain_governors")){ Remove-Item -Path (Join-Path $Repo "receipts\domain_governors") -Recurse -Force -ErrorAction SilentlyContinue }
if(Test-Path $tempDir){ Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host "AION_DOMAIN_GOVERNORS_V1_VERIFY_OK"
