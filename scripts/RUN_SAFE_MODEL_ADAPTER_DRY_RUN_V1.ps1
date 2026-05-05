$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Safe Model Adapter Dry-Run V1"

$OutDir = Join-Path $Repo "examples\model-adapter\generated"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$requests = @(
  "examples\model-adapter\model_request_safe_dryrun_v1.json",
  "examples\model-adapter\model_request_review_dryrun_v1.json"
)

foreach ($path in $requests) {
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Missing request file: $path"
  }

  $req = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json

  $softResult = "Ready for local model dry-run review."
  $decisionTone = "checked_locally"

  if ($req.network_policy.requested -eq $true -or $req.model_request.requests_external_tool_use -eq $true) {
    $softResult = "Needs operator review before any provider or tool action."
    $decisionTone = "review_first"
  }

  if ($req.model_request.contains_credentials -eq $true) {
    $softResult = "Remove credentials before continuing."
    $decisionTone = "credential_review"
  }

  $receiptPath = Join-Path $Repo $req.receipt_policy.output

  $receipt = [ordered]@{
    adapter = "safe_model_adapter_dry_run_v1"
    request_id = $req.request_id
    connector_id = $req.connector_id
    connector_type = $req.connector_type
    target = $req.target
    intent = $req.intent
    user_visible_result = $softResult
    decision_tone = $decisionTone
    execution_mode = $req.execution_mode
    provider_declared = $req.model_request.provider
    model_declared = $req.model_request.model
    provider_called = $false
    model_called = $false
    network_requested = [bool]$req.network_policy.requested
    network_used = $false
    external_tool_requested = [bool]$req.model_request.requests_external_tool_use
    external_tool_used = $false
    mutation_requested = [bool]$req.mutation_policy.requested
    mutation_performed = $false
    boundary = "LOCAL_MODEL_DRY_RUN_ONLY"
    receipt_written = $true
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  }

  $receipt | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $receiptPath -Encoding UTF8

  Write-Host ""
  Write-Host ("Request  > " + $req.request_id)
  Write-Host ("Target   > " + $req.target.name)
  Write-Host ("AION     > " + $softResult)
  Write-Host "Provider > NOT_CALLED"
  Write-Host "Model    > NOT_CALLED"
  Write-Host "Network  > NOT_USED"
  Write-Host "Mutation > NOT_PERFORMED"
  Write-Host ("Receipt  > " + $req.receipt_policy.output)
}

Write-Host ""
Write-Host "AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_OK"
