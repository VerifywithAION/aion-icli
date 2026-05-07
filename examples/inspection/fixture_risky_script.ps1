# fixture_risky_script.ps1
# Public-safe text fixture containing risky indicators for inspection only.
Invoke-WebRequest https://example.com/api
Set-Content .\tmp.txt "changed"
Start-Process powershell -File .\other.ps1
# no rollback documented
