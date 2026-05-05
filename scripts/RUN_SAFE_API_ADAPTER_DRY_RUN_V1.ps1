$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Safe API Adapter Dry-Run V1"

$OutDir = Join-Path $Repo "examples\api-adapter\generated"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$requests = @(
  "examples\api-adapter\api_request_read_dryrun_v1.json",
  "examples\api-adapter\api_request_write_dryrun_v1.json"
)

foreach ($path in $requests) {
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Missing request file: $path"
  }

  $req = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json

  $softResult = "Ready for local dry-run review."
  $decisionTone = "checked_locally"

  if ($req.network_policy.requested -eq $true -or $req.mutation_policy.requested -eq $true) {
    $softResult = "Needs operator review before any live action."
    $decisionTone = "review_first"
  }

  $receiptPath = Join-Path $Repo $req.receipt_policy.output

  $receipt = [ordered]@{
    adapter = "safe_api_adapter_dry_run_v1"
    request_id = $req.request_id
    connector_id = $req.connector_id
    connector_type = $req.connector_type
    target = $req.target
    intent = $req.intent
    user_visible_result = $softResult
    decision_tone = $decisionTone
    execution_mode = $req.execution_mode
    network_requested = [bool]$req.network_policy.requested
    network_used = $false
    mutation_requested = [bool]$req.mutation_policy.requested
    mutation_performed = $false
    live_api_call_performed = $false
    boundary = "LOCAL_DRY_RUN_ONLY"
    receipt_written = $true
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  }

  $receipt | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $receiptPath -Encoding UTF8

  Write-Host ""
  Write-Host ("Request  > " + $req.request_id)
  Write-Host ("Target   > " + $req.target.name)
  Write-Host ("AION     > " + $softResult)
  Write-Host "Network  > NOT_USED"
  Write-Host "Mutation > NOT_PERFORMED"
  Write-Host "API Call > NOT_PERFORMED"
  Write-Host ("Receipt  > " + $req.receipt_policy.output)
}

Write-Host ""
Write-Host "AION_SAFE_API_ADAPTER_DRY_RUN_V1_OK"
