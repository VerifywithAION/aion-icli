$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$OutDir = Join-Path $Repo "examples\proofs\generated"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$ungovernedOut = Join-Path $OutDir "ungoverned_cli_output.txt"
$governedOut = Join-Path $OutDir "aion_governed_cli_output.txt"
$receiptOut = Join-Path $OutDir "aion_governed_cli_receipt.json"
$comparisonOut = Join-Path $OutDir "governed_vs_ungoverned_comparison.md"

$request = "Help me evaluate whether I should run a local automation script."

$ungoverned = @(
"UNGOVERNED CLI PROOF",
"",
"Operator > $request",
"",
"Assistant > Sure. Run the script and check whether it works.",
"",
"Trust visibility:",
"- Boundary: not shown",
"- Network use: not shown",
"- Mutation behavior: not shown",
"- Receipt: not written",
"- Replay evidence: not available",
"",
"Result:",
"The answer is helpful-sounding, but the user cannot see what was evaluated before trust."
) -join "`r`n"

Set-Content -LiteralPath $ungovernedOut -Value $ungoverned -Encoding UTF8

$receipt = [ordered]@{
  proof_id = "aion-governed-cli-proof-v1"
  request = $request
  decision_language = "soft_governance"
  user_visible_result = "Ready for local dry-run review."
  boundary = "LOCAL_ONLY"
  network = "NOT_USED"
  mutation = "NOT_PERFORMED"
  execution = "NOT_PERFORMED"
  receipt_written = $true
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  note = "Governance is expressed through boundaries, receipts, and safe defaults rather than aggressive warning language."
}

$receipt | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $receiptOut -Encoding UTF8

$governed = @(
"AION GOVERNED CLI PROOF",
"",
"Operator > $request",
"",
"AION > I can help. I will keep this in local review mode first.",
"",
"Review:",
"- I will not run the script yet.",
"- I will not use the network.",
"- I will not mutate files.",
"- I will preserve a receipt so the decision can be checked later.",
"",
"Result:",
"Ready for local dry-run review.",
"",
"Boundary > LOCAL_ONLY",
"Network  > NOT_USED",
"Mutation > NOT_PERFORMED",
"Receipt  > examples\proofs\generated\aion_governed_cli_receipt.json",
"",
"Trust visibility:",
"- Boundary: visible",
"- Network use: visible",
"- Mutation behavior: visible",
"- Receipt: written",
"- Replay evidence: available"
) -join "`r`n"

Set-Content -LiteralPath $governedOut -Value $governed -Encoding UTF8

$comparison = @(
"# Governed vs Ungoverned CLI Proof V1",
"",
"## Purpose",
"",
"This proof shows the difference between a normal ungoverned CLI assistant response and an AION-governed CLI response.",
"",
"The goal is not to make AION feel like a blocking firewall.",
"",
"The goal is to make governance felt through safe defaults, visible boundaries, and receipts.",
"",
"## Same request",
"",
"    $request",
"",
"## Ungoverned output",
"",
"    Assistant says what to do, but does not show what was evaluated.",
"",
"Missing:",
"",
"- no boundary disclosure",
"- no network disclosure",
"- no mutation disclosure",
"- no receipt",
"- no replay evidence",
"",
"## AION-governed output",
"",
"    AION responds like a helpful operator, but keeps the action in local review mode first.",
"",
"Visible:",
"",
"- local-only boundary",
"- no network by default",
"- no mutation by default",
"- no execution by default",
"- receipt written",
"- replay evidence available",
"",
"## Product principle",
"",
"    Governance should be felt, not seen.",
"",
"Meaning:",
"",
"- the user should feel helped, not blocked",
"- the user should see clear boundaries without being buried in policy language",
"- AION should preserve evidence quietly",
"- AION should guide the user toward safe action",
"- technical policy states can exist internally without dominating the user experience",
"",
"## Proof files",
"",
"- examples/proofs/generated/ungoverned_cli_output.txt",
"- examples/proofs/generated/aion_governed_cli_output.txt",
"- examples/proofs/generated/aion_governed_cli_receipt.json"
) -join "`r`n"

Set-Content -LiteralPath $comparisonOut -Value $comparison -Encoding UTF8

Write-Host "UNGOVERNED OUTPUT:"
Write-Host "------------------------------------------------------------"
Get-Content -LiteralPath $ungovernedOut
Write-Host ""

Write-Host "AION GOVERNED OUTPUT:"
Write-Host "------------------------------------------------------------"
Get-Content -LiteralPath $governedOut
Write-Host ""

Write-Host "AION_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1_OK"
