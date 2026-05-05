$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI SDK Examples V1"

$OutDir = Join-Path $Repo "examples\sdk\generated"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$requests = @(
  "examples\sdk\sdk_request_safe_read_v1.json",
  "examples\sdk\sdk_request_review_write_v1.json",
  "examples\sdk\sdk_request_model_envelope_v1.json",
  "examples\sdk\sdk_request_api_envelope_v1.json"
)

foreach ($path in $requests) {
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Missing SDK request file: $path"
  }

  $req = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json

  $result = "Ready for local SDK dry-run review."
  $tone = "checked_locally"

  if ($req.network_requested -eq $true) {
    $result = "Needs operator review before any network action."
    $tone = "review_first"
  }

  if ($req.mutation_requested -eq $true) {
    $result = "Needs operator review before any file mutation."
    $tone = "review_first"
  }

  if (($req.PSObject.Properties.Name -contains "provider_call_requested") -and $req.provider_call_requested -eq $true) {
    $result = "Needs operator review before any model provider call."
    $tone = "review_first"
  }

  if (($req.PSObject.Properties.Name -contains "api_call_requested") -and $req.api_call_requested -eq $true) {
    $result = "Needs operator review before any live API call."
    $tone = "review_first"
  }

  $receiptPath = Join-Path $Repo $req.receipt_output

  $receipt = [ordered]@{
    adapter = "sdk_examples_v1"
    request_id = $req.request_id
    sdk_client = $req.sdk_client
    intent = $req.intent
    action = $req.action
    user_visible_result = $result
    decision_tone = $tone
    network_requested = [bool]$req.network_requested
    network_used = $false
    mutation_requested = [bool]$req.mutation_requested
    mutation_performed = $false
    execution_requested = [bool]$req.execution_requested
    execution_performed = $false
    provider_called = $false
    api_called = $false
    boundary = "LOCAL_SDK_DRY_RUN_ONLY"
    receipt_written = $true
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  }

  $receipt | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $receiptPath -Encoding UTF8

  Write-Host ""
  Write-Host ("SDK Request > " + $req.request_id)
  Write-Host ("Action      > " + $req.action.name)
  Write-Host ("AION        > " + $result)
  Write-Host "Network     > NOT_USED"
  Write-Host "Mutation    > NOT_PERFORMED"
  Write-Host "Execution   > NOT_PERFORMED"
  Write-Host "Provider    > NOT_CALLED"
  Write-Host "API         > NOT_CALLED"
  Write-Host ("Receipt     > " + $req.receipt_output)
}

Write-Host ""
Write-Host "AION_SDK_EXAMPLES_V1_OK"
