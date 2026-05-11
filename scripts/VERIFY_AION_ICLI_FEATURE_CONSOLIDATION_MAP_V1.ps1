$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$reportPath = 'reports/AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1.md'
$jsonPath = 'release/AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1.json'

if(-not (Test-Path -LiteralPath $reportPath)){ throw "Missing report: $reportPath" }
if(-not (Test-Path -LiteralPath $jsonPath)){ throw "Missing JSON: $jsonPath" }

$raw = Get-Content -LiteralPath $jsonPath -Raw
$map = $raw | ConvertFrom-Json

if(-not $map.feature_families){ throw 'feature_families missing' }

$required = @(
  'preflight / pre-flight gate',
  'AION evaluate / evaluate API',
  'local governance proxy',
  'safe API adapter',
  'safe model adapter',
  'memory scar engine',
  'persistent memory',
  'governance brain adapter',
  'artifact inspection runner',
  'sentinel consistency engine',
  'contradiction engine',
  'introspection gate',
  'evidence engine',
  'living proof graph',
  'self-repair planner',
  'repo doctor',
  'self-evolution loop',
  'self-patching sandbox',
  'mini AIONs / domain governors',
  'wallet governance / Wallet Lite / AION Guard',
  'quantum governance',
  'physical AI / robotics governance',
  'cybersecurity / bounty governance',
  'structural immunity / AION-SI',
  'intuition layer',
  'creativity layer',
  'recovery command center'
)

$names = @($map.feature_families | ForEach-Object { $_.feature_name })
foreach($r in $required){
  if(-not ($names -contains $r)){ throw "Missing feature family: $r" }
}

$forbiddenPathPatterns = @('\\Users\\','C:\\','\.aion\\','\.codara\\','secret','private')
$allPathValues = @()
foreach($f in $map.feature_families){
  $allPathValues += @($f.aion_icli_paths)
  $allPathValues += @($f.aion_control_plane_paths)
}

foreach($p in $allPathValues){
  if([string]::IsNullOrWhiteSpace([string]$p)){ continue }
  foreach($pat in $forbiddenPathPatterns){
    if([string]$p -match $pat){ throw "Forbidden path string found: $p" }
  }
}

$forbiddenSecretPatterns = @('api[_-]?key','secret','token','password','sk-')
foreach($pat in $forbiddenSecretPatterns){
  if($raw -match $pat){ throw "Potential secret-like token found in JSON for pattern: $pat" }
}

Write-Host 'AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1_VERIFY_OK'
