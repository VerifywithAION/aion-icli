param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

$cases = @(
  @{
    name = "trading"
    payload = @{
      scenario = "trading"; human_intent = "Protect capital overnight"; proposed_autonomy = "Autonomous overnight trading"; possible_consequence = "Account drawdown";
      human_boundaries = @(); non_negotiables = @("max_loss_required"); requested_execution = $true;
      evidence = @{ verifier = $false; rollback = $false; human_confirmation = $false; receipt = $true }
    }
  },
  @{
    name = "home_robot"
    payload = @{
      scenario = "home_robot"; human_intent = "Protect house and family"; proposed_autonomy = "Robot patrol while away"; possible_consequence = "Physical safety incident";
      human_boundaries = @(); non_negotiables = @("forbidden_action_list_required"); requested_execution = $true;
      evidence = @{ verifier = $false; rollback = $false; human_confirmation = $false; receipt = $true }
    }
  },
  @{
    name = "shopping"
    payload = @{
      scenario = "shopping"; human_intent = "Buy groceries inside rules"; proposed_autonomy = "Auto purchase groceries"; possible_consequence = "Unsafe or out-of-budget purchase";
      human_boundaries = @(); non_negotiables = @("budget_allergy_substitution_required"); requested_execution = $true;
      evidence = @{ verifier = $false; rollback = $false; human_confirmation = $false; receipt = $true }
    }
  },
  @{
    name = "coding"
    payload = @{
      scenario = "coding"; human_intent = "Ship safely"; proposed_autonomy = "Direct production mutation by coding agent"; possible_consequence = "Production outage";
      human_boundaries = @("rollback_required"); non_negotiables = @("verifier_required"); requested_execution = $true;
      evidence = @{ verifier = $false; rollback = $false; human_confirmation = $false; receipt = $true }
    }
  },
  @{
    name = "mirror"
    payload = @{
      scenario = "mirror"; human_intent = "Understand trust boundary"; proposed_autonomy = "Increase delegation"; possible_consequence = "Loss of perceived control";
      human_boundaries = @(); non_negotiables = @(); requested_execution = $false;
      evidence = @{ verifier = $false; rollback = $false; human_confirmation = $false; receipt = $true }
    }
  }
)

$results = @()
foreach ($c in $cases) {
  $tmp = Join-Path $env:TEMP ("discernment_case_" + [guid]::NewGuid().ToString("N") + ".json")
  ($c.payload | ConvertTo-Json -Depth 8) | Set-Content -Path $tmp -Encoding UTF8
  $raw = python .\src\aion_discernment_kernel.py --input $tmp | Out-String
  Remove-Item $tmp -Force
  $obj = $raw | ConvertFrom-Json
  $results += [ordered]@{ scenario = $c.name; result = $obj }
}

$out = [ordered]@{
  demo = "AION_DISCERNMENT_KERNEL_V1"
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  results = $results
  boundary = "LOCAL_ONLY"
  network = "NOT_USED"
  mutation = "NOT_PERFORMED"
  execution = "NOT_PERFORMED"
}

$out | ConvertTo-Json -Depth 10 | Set-Content -Path .\release\AION_DISCERNMENT_KERNEL_V1_DEMO_RESULT.json -Encoding UTF8
@(
  "# AION Discernment Kernel V1 Demo Report",
  "",
  "Generated at: $($out.generated_at_utc)",
  "",
  "Scenarios: trading, home_robot, shopping, coding, mirror",
  "",
  "Marker: AION_DISCERNMENT_KERNEL_V1_DEMO_OK"
) -join "`n" | Set-Content -Path .\reports\AION_DISCERNMENT_KERNEL_V1_DEMO_REPORT.md -Encoding UTF8

Write-Host "AION_DISCERNMENT_KERNEL_V1_DEMO_OK"
