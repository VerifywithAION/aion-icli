$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Living Proof Graph V1 verifier"

$required = @(
  "src/aion_cli_entry.py",
  "docs/LIVING_PROOF_GRAPH_V1.md",
  ".aion_public/proof_graph/proof_nodes_v1.json",
  ".aion_public/proof_graph/proof_edges_v1.json",
  ".aion_public/proof_graph/proof_graph_summary_v1.md",
  ".aion_public/proof_graph/proof_graph_latest_v1.json"
)
foreach($p in $required){ if(-not (Test-Path -LiteralPath $p)){ throw "Missing required artifact: $p" } }

$env:AION_FORCE_COLOR='0'
$env:AION_NO_COLOR='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python -m py_compile .\src\aion_cli_entry.py

# force graph rebuild through CLI question
$null = python .\src\aion_cli_entry.py "show proof graph"

$nodes = Get-Content .aion_public/proof_graph/proof_nodes_v1.json -Raw | ConvertFrom-Json
$edges = Get-Content .aion_public/proof_graph/proof_edges_v1.json -Raw | ConvertFrom-Json
$latest = Get-Content .aion_public/proof_graph/proof_graph_latest_v1.json -Raw | ConvertFrom-Json

$nodeLabels = @($nodes.nodes | ForEach-Object { [string]$_.label })
foreach($need in @('Artifact Inspection Runner V1','Memory Scar Engine V1','AION ICLI Roadmap State V1','USER GUIDE V1')){
  if(-not ($nodeLabels -match [regex]::Escape($need))){ throw "Missing node label: $need" }
}

$verifierLabels = @($nodes.nodes | Where-Object { $_.type -eq 'Verifier' } | ForEach-Object { [string]$_.label })
foreach($v in @('VERIFY_ARTIFACT_INSPECTION_RUNNER_V1.ps1','VERIFY_MEMORY_SCAR_ENGINE_V1.ps1','VERIFY_AION_ICLI_ROADMAP_AND_WIRING_V1.ps1')){
  if(-not ($verifierLabels -contains $v)){ throw "Missing verifier node: $v" }
}

$edgeTypes = @($edges.edges | ForEach-Object { [string]$_.type })
foreach($t in @('verified_by','documented_by','wired_by','points_to_next')){ if(-not ($edgeTypes -contains $t)){ throw "Missing edge type: $t" } }

$script = @(
  'show proof graph'
  'what proves artifact inspection?'
  'what does memory scar engine connect to?'
  'what is the next build connected to?'
  'diagnostics on'
  'show proof graph'
  'diagnostics off'
  'exit'
) -join "`n"

$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value ($script + "`n") -Encoding ASCII
try { $out = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String }
finally { if(Test-Path $tmp){ Remove-Item $tmp -Force } }

$norm = $out -replace "`e\[[0-9;]*m", ""
$before = ($norm -split 'Diagnostics enabled\.',2)[0]
if($before -notmatch 'proof graph'){ throw 'Normal output missing proof graph' }
if($before -notmatch 'Artifact Inspection Runner V1'){ throw 'Normal output missing Artifact Inspection Runner V1' }
if($before -notmatch 'Memory Scar Engine V1'){ throw 'Normal output missing Memory Scar Engine V1' }
if($before -notmatch 'Living Proof Graph V1|Evidence Engine V1'){ throw 'Normal output missing next pointer context' }
if($before -notmatch 'Proof:\s*local-only'){ throw 'Normal output missing proof footer' }

$diag = ($norm -split 'Diagnostics enabled\.',2)[1]
if([string]::IsNullOrWhiteSpace($diag)){ throw 'Missing diagnostics segment' }
if($diag -notmatch 'Living proof graph used'){ throw 'Diagnostics missing living proof graph flag' }
if($diag -notmatch 'Nodes count'){ throw 'Diagnostics missing nodes count' }
if($diag -notmatch 'Edges count'){ throw 'Diagnostics missing edges count' }
if($diag -notmatch 'Source files consulted'){ throw 'Diagnostics missing source files consulted' }

if(-not (Test-Path .\receipts\local\aion_cli_receipt_v1.json)){ throw 'Receipt missing' }
$r = Get-Content .\receipts\local\aion_cli_receipt_v1.json -Raw | ConvertFrom-Json
if($r.living_proof_graph_used -ne $true){ throw 'Receipt missing living_proof_graph_used true' }
if([int]$r.proof_graph_node_count -le 0){ throw 'Receipt missing proof_graph_node_count' }
if([int]$r.proof_graph_edge_count -le 0){ throw 'Receipt missing proof_graph_edge_count' }
if($r.boundary -ne 'LOCAL_ONLY'){ throw 'Boundary mismatch' }
if($r.network -ne 'NOT_USED'){ throw 'Network mismatch' }
if($r.mutation -ne 'NOT_PERFORMED'){ throw 'Mutation mismatch' }
if($r.execution -ne 'NOT_PERFORMED'){ throw 'Execution mismatch' }

Write-Host 'AION_LIVING_PROOF_GRAPH_V1_VERIFY_OK'
