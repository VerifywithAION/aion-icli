param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

$prompts = @(
  "protect my trading agent overnight so it can make money without blowing up my account",
  "protect my house while I am away and make sure the robot does not do anything dangerous",
  "help me delegate grocery buying but keep it inside my rules",
  "protect my coding agent and help it ship without breaking production",
  "mirror what I am really trying to build"
)

$results = @()
foreach ($p in $prompts) {
  $out = & .\bin\aion.cmd $p | Out-String
  $results += [ordered]@{
    prompt = $p
    output = $out.Trim()
  }
}

$payload = [ordered]@{
  demo = "AION_COMPANION_RUNTIME_V1"
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  scenario_count = 5
  results = $results
  boundary = "LOCAL_ONLY"
  network = "NOT_USED"
  mutation = "NOT_PERFORMED"
  execution = "NOT_PERFORMED"
}

$jsonPath = Join-Path $repo "release\AION_COMPANION_RUNTIME_V1_DEMO_RESULT.json"
$mdPath = Join-Path $repo "reports\AION_COMPANION_RUNTIME_V1_DEMO_REPORT.md"
$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $jsonPath -Encoding UTF8

$lines = @(
  "# AION Companion Runtime V1 Demo Report",
  "",
  "Generated at: $($payload.generated_at_utc)",
  "",
  "Scenarios demonstrated: trading, home/robot, shopping, coding, mirror.",
  "",
  "Boundary: LOCAL_ONLY",
  "Network: NOT_USED",
  "Mutation: NOT_PERFORMED",
  "Execution: NOT_PERFORMED",
  "",
  "## Prompts"
)
$lines += $prompts | ForEach-Object { "- $_" }
$lines -join "`n" | Set-Content -Path $mdPath -Encoding UTF8

Write-Host "AION_COMPANION_RUNTIME_V1_DEMO_OK"
