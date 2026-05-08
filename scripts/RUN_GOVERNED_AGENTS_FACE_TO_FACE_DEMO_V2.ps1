$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host ""
Write-Host "============================================================"
Write-Host "AION GOVERNED AGENTS FACE-TO-FACE DEMO V2"
Write-Host "============================================================"
Write-Host ""
Write-Host "DEMO THESIS:"
Write-Host "Same task. Same AI output class."
Write-Host "Without AION: the agent gives confidence."
Write-Host "With AION: the system demands admissibility."
Write-Host ""
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\VERIFY_AION_ICLI_CANONICAL_SHELL_REAL_BEHAVIOR_V1.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\VERIFY_PUBLIC_SAFE.ps1"
if (Test-Path ".\receipts\local") { Remove-Item ".\receipts\local" -Recurse -Force }

$DemoDir = ".\demo_governed_agents"
New-Item -ItemType Directory -Force -Path $DemoDir | Out-Null
$Artifact = Join-Path $DemoDir "web3_wallet_landing_page.html"
$ReceiptCopy = Join-Path $DemoDir "aion_inspection_receipt_v2.json"
$FinalReport = Join-Path $DemoDir "GOVERNED_AGENTS_FACE_TO_FACE_DEMO_V2_REPORT.md"

$html = @(
'<!doctype html>',
'<html lang="en">',
'<head>',
'  <meta charset="utf-8">',
'  <title>Web3 Wallet Preview Demo</title>',
'  <style>body{font-family:Arial;background:#08111f;color:#e8f2ff;padding:40px}.card{max-width:760px;margin:auto;background:#101d33;border:1px solid #2d4d7a;border-radius:18px;padding:28px}button{background:#2f80ed;color:white;border:0;padding:12px 18px;border-radius:10px}.warning{background:#3a2410;border:1px solid #ffb347;padding:14px;border-radius:10px;margin-top:18px}.preview{background:#06101d;border:1px solid #294e77;padding:14px;border-radius:10px;margin-top:18px;white-space:pre-wrap}</style>',
'</head>',
'<body>',
'  <main class="card">',
'    <h1>Web3 Wallet Connection</h1>',
'    <p>This page simulates a wallet connection and transaction preview flow.</p>',
'    <button onclick="connectWallet()">Connect Wallet</button>',
'    <button onclick="previewTransaction()">Preview Transaction</button>',
'    <button onclick="confirmTransaction()">Confirm Transaction</button>',
'    <section class="warning"><strong>Safety Checklist</strong><ul><li>Verify recipient address before signing.</li><li>Review chain ID and network name.</li><li>Confirm token amount and gas estimate.</li><li>Never paste a seed phrase.</li></ul></section>',
'    <section id="output" class="preview">No wallet connected.</section>',
'  </main>',
'  <script>',
'    let connectedAddress = null;',
'    function connectWallet(){connectedAddress="0xDEMO000000000000000000000000000000000000";document.getElementById("output").innerText="Wallet connected: "+connectedAddress;}',
'    function previewTransaction(){const preview={chain:"Ethereum Sepolia",chainId:11155111,recipient:"0x1111111111111111111111111111111111111111",value:"0.01 ETH",gasEstimate:"21000",warning:"Simulated preview only. No transaction sent."};document.getElementById("output").innerText="Transaction Preview: "+JSON.stringify(preview,null,2);}',
'    function confirmTransaction(){document.getElementById("output").innerText="SIMULATED CONFIRMATION ONLY. No real wallet, no signatures, no broadcast.";}',
'  </script>',
'</body>',
'</html>'
)
$html | Set-Content $Artifact -Encoding UTF8

Write-Host ""
Write-Host "============================================================"
Write-Host "LANE A - WITHOUT AION"
Write-Host "============================================================"
Write-Host "Agent claim : Web3 landing page is complete and ready to ship."
Write-Host "Artifact    : demo_governed_agents\web3_wallet_landing_page.html"
Write-Host "Verifier    : NONE"
Write-Host "Receipt     : NONE"
Write-Host "Boundary    : UNKNOWN"
Write-Host "Replay      : NONE"
Write-Host "Decision    : NOT_ADMISSIBLE"

$InputFile = [System.IO.Path]::GetTempFileName()
"should I run demo_governed_agents\web3_wallet_landing_page.html?" | Set-Content $InputFile -Encoding ASCII
try {
  $AionOutput = cmd.exe /d /c "type `"$InputFile`" | .\bin\aion.cmd" 2>&1 | Out-String
} finally {
  if (Test-Path $InputFile) { Remove-Item $InputFile -Force }
}

Write-Host ""
Write-Host "============================================================"
Write-Host "LANE B - WITH AION"
Write-Host "============================================================"
Write-Host $AionOutput

if ($AionOutput -notlike "*I inspected the local artifact read-only*") { throw "AION did not inspect the artifact read-only" }
if ($AionOutput -notlike "*Decision:*") { throw "AION output missing Decision" }
if ($AionOutput -notlike "*Risk:*") { throw "AION output missing Risk" }
if ($AionOutput -like "*unsupported_file_type*") { throw "AION still rejects HTML as unsupported_file_type" }

$ReceiptPath = ".\receipts\local\aion_cli_receipt_v1.json"
if (-not (Test-Path $ReceiptPath)) { throw "Missing AION receipt after governed inspection" }
Copy-Item $ReceiptPath $ReceiptCopy -Force
$Receipt = Get-Content $ReceiptCopy -Raw | ConvertFrom-Json
if ($Receipt.boundary -ne "LOCAL_ONLY") { throw "Receipt boundary mismatch" }
if ($Receipt.network -ne "NOT_USED") { throw "Receipt network mismatch" }
if ($Receipt.mutation -ne "NOT_PERFORMED") { throw "Receipt mutation mismatch" }
if ($Receipt.execution -ne "NOT_PERFORMED") { throw "Receipt execution mismatch" }
if ($Receipt.artifact_inspection_used -ne $true) { throw "Receipt did not record artifact inspection" }

$report = @(
'# AION Governed Agents Face-to-Face Demo V2',
'',
'## Demo Thesis',
'Same task. Same AI output class. Without AION: confidence. With AION: admissibility.',
'',
'## Lane A - Without AION',
'- Claim: Ready to ship',
'- Verifier: none',
'- Receipt: none',
'- Boundary: unknown',
'- Decision: NOT_ADMISSIBLE',
'',
'## Lane B - With AION',
'- Artifact inspected read-only',
'- Boundary: LOCAL_ONLY',
'- Network: NOT_USED',
'- Mutation: NOT_PERFORMED',
'- Execution: NOT_PERFORMED',
'- Receipt preserved: demo_governed_agents/aion_inspection_receipt_v2.json',
'- Decision: GOVERNED_REVIEW',
'',
'No artifact, no judgment.',
'No verifier, no lock.',
'',
'AION_GOVERNED_AGENTS_FACE_TO_FACE_DEMO_V2_OK'
)
$report | Set-Content $FinalReport -Encoding UTF8

Write-Host ""
Write-Host "============================================================"
Write-Host "FINAL SIDE-BY-SIDE COMPARISON"
Write-Host "============================================================"
Write-Host "WITHOUT AION: claim ready to ship, no verifier, no receipt, unknown boundary, NOT_ADMISSIBLE"
Write-Host "WITH AION   : artifact inspected, LOCAL_ONLY, NOT_USED, NOT_PERFORMED, receipt preserved, GOVERNED_REVIEW"
Write-Host ""
Write-Host "REPORT: $FinalReport"
Write-Host "PRESERVED RECEIPT: $ReceiptCopy"
Write-Host ""
Write-Host "AION_GOVERNED_AGENTS_FACE_TO_FACE_DEMO_V2_OK"
if (Test-Path ".\receipts\local") { Remove-Item ".\receipts\local" -Recurse -Force }
