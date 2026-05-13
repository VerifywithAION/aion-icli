param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-live-demo"
Set-Location $repo

$prompts = @(
  "what is a genius-level governance question for this system?",
  "give a governance-aware answer about release readiness",
  "continue from that and reframe the highest-risk assumption",
  "what are you uncertain about right now?",
  "show a non-obvious but grounded next move"
)

$captures = @()
foreach($p in $prompts){
  $out = & .\bin\aion.cmd $p | Out-String
  $captures += [pscustomobject]@{ prompt=$p; output=$out }
}

$receiptPath = Join-Path $repo "receipts\local\aion_cli_receipt_v1.json"
$receipt = $null
if(Test-Path $receiptPath){
  $receipt = Get-Content -Raw -Path $receiptPath | ConvertFrom-Json
}

$result = [ordered]@{
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  adapter = "AION_LIVING_VOICE_ADAPTER_V1"
  captures = $captures
  receipt_path = "receipts/local/aion_cli_receipt_v1.json"
  receipt_capability = if($receipt){$receipt.capability}else{"missing"}
  local_only = if($receipt){$receipt.boundary}else{"unknown"}
  network = if($receipt){$receipt.network}else{"unknown"}
}

$resultPath = Join-Path $repo "release\AION_LIVING_VOICE_ADAPTER_V1_DEMO_RESULT.json"
$reportPath = Join-Path $repo "reports\AION_LIVING_VOICE_ADAPTER_V1_DEMO_REPORT.md"

$result | ConvertTo-Json -Depth 10 | Set-Content -Path $resultPath -Encoding UTF8

$lines = @(
  "# AION Living Voice Adapter V1 Demo Report",
  "",
  "Generated at UTC: $($result.generated_at_utc)",
  "Adapter: AION_LIVING_VOICE_ADAPTER_V1",
  "",
  "## Prompt set"
)
foreach($c in $captures){
  $lines += "- Prompt: $($c.prompt)"
  $lines += "  - Output contains continuity framing: $([bool]($c.output -match 'Continuity note|continuity'))"
  $lines += "  - Output contains bounded truth language: $([bool]($c.output -match 'cannot guarantee|uncertainty|partial'))"
}
$lines += ""
$lines += "Receipt capability: $($result.receipt_capability)"
$lines += "Boundary: $($result.local_only)"
$lines += "Network: $($result.network)"
$lines += ""
$lines += "Marker: AION_LIVING_VOICE_ADAPTER_V1_DEMO_OK"
$lines -join "`r`n" | Set-Content -Path $reportPath -Encoding UTF8

Write-Host "AION_LIVING_VOICE_ADAPTER_V1_DEMO_OK"
