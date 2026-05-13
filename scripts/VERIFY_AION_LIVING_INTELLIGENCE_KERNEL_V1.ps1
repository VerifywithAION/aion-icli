param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

if (!(Test-Path .\src\aion_living_intelligence_kernel.py)) { throw "Missing kernel source" }
python -m py_compile .\src\aion_living_intelligence_kernel.py
python -m py_compile .\src\aion_cli_entry.py

$prompts = @(
  "ask aion can I ship this wallet helper?",
  "ask aion what is the core truth of AION?",
  "ask aion what am I missing if AION still feels like a toy?",
  "investigate why local models gave confident wrong answers",
  "what is the next best question for finishing AION ICLI?"
)

foreach($p in $prompts){
  $out = & .\bin\aion.cmd $p | Out-String
  if($out -notmatch "Direct truth|direct_truth"){ throw "Missing direct truth block" }
  if($out -notmatch "Next best question|next_best_question"){ throw "Missing next best question block" }
  if($out -notmatch "Governed answer|governed_answer"){ throw "Missing governed answer block" }
  if($out -notmatch "Next admissible move|next_admissible_move"){ throw "Missing next admissible move block" }
  if($out -notmatch "LOCAL_ONLY"){ throw "Missing LOCAL_ONLY posture" }
  if($out -notmatch "NOT_USED"){ throw "Missing NOT_USED posture" }
  if($out -notmatch "NOT_PERFORMED"){ throw "Missing NOT_PERFORMED posture" }
}

$receiptDir = Join-Path $repo "receipts\living_intelligence"
if(!(Test-Path $receiptDir)){ throw "Living intelligence receipt folder missing" }
$latest = Get-ChildItem -Path $receiptDir -File | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1
if(-not $latest){ throw "No living intelligence receipts found" }
$payload = Get-Content -Raw -Path $latest.FullName | ConvertFrom-Json
if([string]::IsNullOrWhiteSpace($latest.FullName)){ throw "latest receipt path missing" }
if(!(Test-Path $latest.FullName)){ throw "latest receipt not found" }
if([string]::IsNullOrWhiteSpace($payload.result.direct_truth)){ throw "receipt result direct_truth missing" }

& powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1 | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_LIVING_VOICE_ADAPTER_V1.ps1 | Out-Null

Write-Host "AION_LIVING_INTELLIGENCE_KERNEL_V1_VERIFY_OK"
