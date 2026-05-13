param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

$prompts = @(
  "ask aion can I ship this wallet helper?",
  "ask aion what is the core truth of AION?",
  "ask aion what am I missing if AION still feels like a toy?",
  "investigate why local models gave confident wrong answers",
  "what is the next best question for finishing AION ICLI?"
)

$caps = @()
foreach($p in $prompts){
  $out = & .\bin\aion.cmd $p | Out-String
  $caps += [pscustomobject]@{ prompt = $p; output = $out }
}

$receiptPath = Join-Path $repo "receipts\living_intelligence"
$latestReceipt = ""
if(Test-Path $receiptPath){
  $latest = Get-ChildItem -Path $receiptPath -File | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1
  if($latest){ $latestReceipt = $latest.FullName }
}

$result = [ordered]@{
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  engine = "AION_LIVING_INTELLIGENCE_KERNEL_V1"
  captures = $caps
  latest_living_intelligence_receipt = $latestReceipt
}

$resultJson = Join-Path $repo "release\AION_LIVING_INTELLIGENCE_KERNEL_V1_DEMO_RESULT.json"
$reportMd = Join-Path $repo "reports\AION_LIVING_INTELLIGENCE_KERNEL_V1_DEMO_REPORT.md"

$result | ConvertTo-Json -Depth 10 | Set-Content -Path $resultJson -Encoding UTF8

$lines = @(
  "# AION Living Intelligence Kernel V1 Demo Report",
  "",
  "Generated at UTC: $($result.generated_at_utc)",
  "Engine: AION_LIVING_INTELLIGENCE_KERNEL_V1",
  "",
  "## Prompt checks"
)
foreach($c in $caps){
  $lines += "- Prompt: $($c.prompt)"
  $lines += "  - contains direct_truth: $([bool]($c.output -match 'Direct truth|direct_truth'))"
  $lines += "  - contains next_best_question: $([bool]($c.output -match 'Next best question|next_best_question'))"
  $lines += "  - contains governed_answer: $([bool]($c.output -match 'Governed answer|governed_answer'))"
  $lines += "  - contains next_admissible_move: $([bool]($c.output -match 'Next admissible move|next_admissible_move'))"
}
$lines += ""
$lines += "Marker: AION_LIVING_INTELLIGENCE_KERNEL_V1_DEMO_OK"
$lines -join "`r`n" | Set-Content -Path $reportMd -Encoding UTF8

Write-Host "AION_LIVING_INTELLIGENCE_KERNEL_V1_DEMO_OK"
