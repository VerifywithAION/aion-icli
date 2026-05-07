$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Roadmap + Wiring V1 verifier"

$required = @(
  "docs/AION_ICLI_ROADMAP_STATE_V1.md",
  "docs/AION_ICLI_NEXT_8_BUILDS_V1.md",
  "docs/AION_ICLI_SYSTEM_WIRING_REPORT_V1.md",
  ".aion_public/roadmap/roadmap_state_v1.json",
  ".aion_public/wiring/system_wiring_v1.json"
)
foreach($p in $required){ if(-not (Test-Path -LiteralPath $p)){ throw "Missing required artifact: $p" } }

$road = Get-Content .aion_public/roadmap/roadmap_state_v1.json -Raw | ConvertFrom-Json
$wire = Get-Content .aion_public/wiring/system_wiring_v1.json -Raw | ConvertFrom-Json

if($road.latest_completed_layer -ne 'Memory Scar Engine V1'){ throw 'latest_completed_layer mismatch' }
if($road.next_build_pointer -ne 'Artifact Inspection Runner V1'){ throw 'next_build_pointer mismatch' }
if($wire.status -notin @('PASS','PARTIAL')){ throw 'Invalid wiring status' }
if($wire.status -eq 'PARTIAL' -and (-not $wire.next_required_action)){ throw 'PARTIAL status requires next_required_action' }

$layers = @($wire.layers)
$requiredLayers = @('Public Safe Verifier','Public Install Package V1','User Guide V1','Interactive Mode V1','Capability Router V1','Voice Layer V1','Adaptive Reasoning Layer V1','Governance Brain Adapter V1','Governance Brain Integration Fix V1','Memory Scar Engine V1')
foreach($l in $requiredLayers){ if(-not ($layers | Where-Object { $_.layer_name -eq $l })){ throw "Missing layer in wiring: $l" } }

$nextDoc = Get-Content docs/AION_ICLI_NEXT_8_BUILDS_V1.md -Raw
$mustNext = @('Artifact Inspection Runner V1','Living Proof Graph V1','Evidence Engine V1','Introspection Gate V1','Contradiction Engine V1','Self-Repair Planner V1','Sentinel Consistency Engine V1','Offline AION CLI Bundle V1')
foreach($n in $mustNext){ if($nextDoc -notmatch [regex]::Escape($n)){ throw "Missing next build item: $n" } }

$roadDoc = Get-Content docs/AION_ICLI_ROADMAP_STATE_V1.md -Raw
if($roadDoc -notmatch 'v1\.0\.0-public-icli' -or $roadDoc -notmatch 'not yet rebuilt'){ throw 'Missing public release caveat' }
if($roadDoc -notmatch 'A layer is complete only if'){ throw 'Missing end-to-end wiring rule' }

Write-Host 'AION_ICLI_ROADMAP_AND_WIRING_V1_VERIFY_OK'

