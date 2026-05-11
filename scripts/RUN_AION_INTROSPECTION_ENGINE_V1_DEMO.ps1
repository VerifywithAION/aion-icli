param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"

$buildRaw = & $Py (Join-Path $Repo "src\aion_introspection_engine.py") build
$build = $buildRaw | ConvertFrom-Json

$demoJson = Join-Path $Repo "release\AION_INTROSPECTION_ENGINE_V1_DEMO_RESULT.json"
$demoMd = Join-Path $Repo "reports\AION_INTROSPECTION_ENGINE_V1_DEMO_REPORT.md"

@{
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  marker = "AION_INTROSPECTION_ENGINE_V1_DEMO_OK"
  result = $build
} | ConvertTo-Json -Depth 20 | Set-Content -Path $demoJson -Encoding UTF8

$lines = @(
  "# AION Introspection Engine V1 Demo Report",
  "",
  "Generated at UTC: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))",
  "Engine: $($build.engine)",
  "Proven count: $($build.summary.proven_count)",
  "Missing count: $($build.summary.missing_count)",
  "Next build pointer: $($build.next_build_pointer)",
  "",
  "Outputs:",
  "- release/AION_LIVING_PROOF_GRAPH_V1.json",
  "- reports/AION_LIVING_PROOF_GRAPH_V1.md",
  "- release/AION_INTROSPECTION_ENGINE_V1_DEMO_RESULT.json",
  "- reports/AION_INTROSPECTION_ENGINE_V1_DEMO_REPORT.md",
  "",
  "Marker: AION_INTROSPECTION_ENGINE_V1_DEMO_OK"
)
$lines -join "`r`n" | Set-Content -Path $demoMd -Encoding UTF8

Write-Host "AION_INTROSPECTION_ENGINE_V1_DEMO_OK"
