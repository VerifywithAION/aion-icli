param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

if (!(Test-Path .\src\aion_dynamic_cognition_engine.py)) { throw "Missing src/aion_dynamic_cognition_engine.py" }
if (!(Test-Path .\scripts\RUN_AION_DYNAMIC_COGNITION_ENGINE_V1_DEMO.ps1)) { throw "Missing demo runner" }

python -m py_compile .\src\aion_dynamic_cognition_engine.py
python -m py_compile .\src\aion_living_intelligence_kernel.py
python -m py_compile .\src\aion_cli_entry.py

$tmpPy = Join-Path $env:TEMP ("aion_dynamic_verify_" + [guid]::NewGuid().ToString("N") + ".py")
$py = @'
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "src"))
from aion_dynamic_cognition_engine import analyze_dynamic_cognition

prompts = [
    "ask aion why does AION still not feel alive?",
    "ask aion what invisible assumption is slowing this project?",
    "investigate why strong local models still produce shallow answers",
    "analyze this deeply: why do most AI systems feel fake?",
    "what question would unlock the next evolution of AION?",
]

results = [analyze_dynamic_cognition(p) for p in prompts]
answers = set()
questions = set()

for r in results:
    assert len(r.get("competing_theories", [])) >= 3, "competing_theories < 3"
    assert r.get("strongest_theory"), "missing strongest_theory"
    assert len(r.get("rejected_theories", [])) >= 1, "missing rejected_theories"
    assert r.get("contradiction_pressure"), "missing contradiction_pressure"
    assert r.get("nonobvious_insight"), "missing nonobvious_insight"
    assert r.get("dynamic_reframe"), "missing dynamic_reframe"
    assert r.get("next_best_question"), "missing next_best_question"
    assert r.get("continuity_update"), "missing continuity_update"
    assert r.get("boundary") == "LOCAL_ONLY", "boundary not LOCAL_ONLY"
    assert r.get("network") == "NOT_USED", "network not NOT_USED"
    assert r.get("mutation") == "NOT_PERFORMED", "mutation not NOT_PERFORMED"
    assert r.get("execution") == "NOT_PERFORMED", "execution not NOT_PERFORMED"
    assert r.get("receipt_written") is True, "receipt_written not true"
    receipt_abs = r.get("receipt_abs_path")
    assert receipt_abs and Path(receipt_abs).exists(), "receipt_abs_path missing"
    answers.add((r.get("governed_answer") or "").strip())
    questions.add((r.get("next_best_question") or "").strip())

assert len(answers) == len(prompts), "repeated governed_answer detected"
assert len(questions) == len(prompts), "next_best_question not prompt-specific"
print("PY_ASSERT_OK")
'@
Set-Content -Path $tmpPy -Value $py -Encoding UTF8
python $tmpPy
Remove-Item $tmpPy -Force

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_DYNAMIC_COGNITION_ENGINE_V1_DEMO.ps1 | Out-Null
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1 | Out-Null
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_LIVING_VOICE_ADAPTER_V1.ps1 | Out-Null
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_LIVING_INTELLIGENCE_KERNEL_V1.ps1 | Out-Null

Write-Host "AION_DYNAMIC_COGNITION_ENGINE_V1_VERIFY_OK"
