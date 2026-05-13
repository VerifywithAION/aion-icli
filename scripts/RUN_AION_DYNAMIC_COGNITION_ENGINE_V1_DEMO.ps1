param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

$outJson = Join-Path $repo "release\AION_DYNAMIC_COGNITION_ENGINE_V1_DEMO_RESULT.json"
$outReport = Join-Path $repo "reports\AION_DYNAMIC_COGNITION_ENGINE_V1_DEMO_REPORT.md"

$prompts = @(
  "ask aion why does AION still not feel alive?",
  "ask aion what invisible assumption is slowing this project?",
  "investigate why strong local models still produce shallow answers",
  "analyze this deeply: why do most AI systems feel fake?",
  "what question would unlock the next evolution of AION?"
)

$results = @()
foreach($p in $prompts){
  $raw = & .\bin\aion.cmd $p | Out-String
  $results += [ordered]@{
    prompt = $p
    cli_output = $raw.Trim()
  }
}

$payload = [ordered]@{
  demo = "AION_DYNAMIC_COGNITION_ENGINE_V1"
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  prompt_count = $prompts.Count
  results = $results
  boundary = "LOCAL_ONLY"
  network = "NOT_USED"
  mutation = "NOT_PERFORMED"
  execution = "NOT_PERFORMED"
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $outJson -Encoding UTF8

$lines = @(
  "# AION Dynamic Cognition Engine V1 Demo Report",
  "",
  "Generated at: $($payload.generated_at_utc)",
  "",
  "Boundary: LOCAL_ONLY",
  "Network: NOT_USED",
  "Mutation: NOT_PERFORMED",
  "Execution: NOT_PERFORMED",
  "",
  "## Prompts"
)
$lines += $prompts | ForEach-Object { "- $_" }
$lines -join "`n" | Set-Content -Path $outReport -Encoding UTF8

Write-Host "AION_DYNAMIC_COGNITION_ENGINE_V1_DEMO_OK"
