param(
  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$Query
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$env:PYTHONUTF8 = "1"
$env:AION_FORCE_COLOR = "1"
$env:PYTHONIOENCODING = "utf-8"

$Repo = Split-Path -Parent $MyInvocation.MyCommand.Definition
$Entry = Join-Path $Repo "src\aion_cli_entry.py"

if (-not (Test-Path -LiteralPath $Entry)) {
  throw "Missing AION public CLI entry: $Entry"
}

if ($Query -and $Query.Count -gt 0) {
  & python $Entry @Query
} else {
  & python $Entry
}

exit $LASTEXITCODE
