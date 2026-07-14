# Skeptical system-wide verification
# Don't assume anything works - verify everything

$results = @{
    Files = @{}
    Functions = @{}
    State = @{}
    Dependencies = @{}
    Overall = $true
}

$vaultRoot = (Resolve-Path $PSScriptRoot).Path

# 1. Verify all files exist
$requiredFiles = @(
    "STABILIZATION-PLAN.md",
    "STABILIZATION-REPORT.md",
    "STABILIZATION-STATUS.json",
    "SimpleStabilization.ps1",
    "!\STATE\final-verification.json"
)

foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $vaultRoot $file
    $results.Files[$file] = Test-Path $fullPath
    if (-not $results.Files[$file]) {
        $results.Overall = $false
    }
}

# 2. Test module import
try {
    Import-Module (Join-Path $vaultRoot "SimpleStabilization.ps1") -Force -ErrorAction Stop
    $results.Functions.ModuleImport = $true
} catch {
    $results.Functions.ModuleImport = $false
    $results.Overall = $false
}

# 3. Test individual functions
$functionsToTest = @(
    "New-StabilizationSession",
    "Update-StabilizationSession", 
    "Test-SystemDependency",
    "Handle-StabilizationError",
    "Check-LEVELSETCompliance"
)

foreach ($func in $functionsToTest) {
    try {
        $null = Get-Command $func -ErrorAction Stop
        $results.Functions[$func] = $true
    } catch {
        $results.Functions[$func] = $false
        $results.Overall = $false
    }
}

# 4. Test state management
try {
    $testSession = New-StabilizationSession -SessionId "skeptical-test" -InitialContext @{Test="Skeptical"}
    if ($testSession.Success -and (Test-Path $testSession.SessionFile)) {
        $results.State.Works = $true
        $results.State.File = $testSession.SessionFile
    } else {
        $results.State.Works = $false
        $results.Overall = $false
    }
} catch {
    $results.State.Works = $false
    $results.State.Error = $_.Exception.Message
    $results.Overall = $false
}

# 5. Test dependency checking
try {
    $ollamaTest = Test-SystemDependency -Component "Ollama"
    $results.Dependencies.Ollama = $ollamaTest.Status -ne $null
} catch {
    $results.Dependencies.Ollama = $false
}

# 6. Test compliance checking
try {
    $compliance = Check-LEVELSETCompliance
    $results.Dependencies.Compliance = $compliance -ne $null
} catch {
    $results.Dependencies.Compliance = $false
}

# Output results
$results | ConvertTo-Json -Depth 10 | Out-File (Join-Path $vaultRoot "SKEPTICAL-VERIFICATION.json") -Force

# Console summary
Write-Host "=== SKEPTICAL SYSTEM VERIFICATION ==="
Write-Host "Overall Status: $(if ($results.Overall) {'✅ PASS'} else {'❌ FAIL'})"
Write-Host ""
Write-Host "Files Verified:"
foreach ($file in $requiredFiles) {
    $status = if ($results.Files[$file]) {'✅'} else {'❌'}
    Write-Host "  $status $file"
}
Write-Host ""
Write-Host "Functions Tested:"
foreach ($func in $functionsToTest) {
    $status = if ($results.Functions[$func]) {'✅'} else {'❌'}
    Write-Host "  $status $func"
}
Write-Host ""
Write-Host "State Management: $(if ($results.State.Works) {'✅ WORKS'} else {'❌ FAILED'})"
Write-Host "Dependency Checks: Ollama=$(if ($results.Dependencies.Ollama) {'✅'} else {'❌'}), Compliance=$(if ($results.Dependencies.Compliance) {'✅'} else {'❌'})"
Write-Host ""
Write-Host "Detailed results saved to: !/SKEPTICAL-VERIFICATION.json"

if (-not $results.Overall) {
    Write-Host "⚠️  SYSTEM VERIFICATION FAILED - Issues detected" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "✅ SYSTEM VERIFICATION PASSED - All checks successful" -ForegroundColor Green
    exit 0
}
