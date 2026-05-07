# Test script for VaultStabilization module

# Import the module
try {
    Import-Module "$PSScriptRoot\VaultStabilization.psm1" -Force -ErrorAction Stop
    Write-Host "✅ Module imported successfully"
}
catch {
    Write-Host "❌ Module import failed: $_"
    exit 1
}

# Test 1: State session initialization
try {
    $testSession = Initialize-StateSession -SessionId "test-001" -Context @{Test="Basic functionality"}
    if ($testSession.Success) {
        Write-Host "✅ State session initialized: $($testSession.StateFile)"
    } else {
        Write-Host "❌ State session failed: $($testSession.Error)"
    }
}
catch {
    Write-Host "❌ State test failed: $_"
}

# Test 2: LEVELSET check
try {
    $levelset = Perform-LEVELSETCheck
    if ($levelset.Valid) {
        Write-Host "✅ LEVELSET check passed"
    } else {
        Write-Host "⚠️  LEVELSET check failed: $($levelset.Issues -join ', ')"
    }
}
catch {
    Write-Host "❌ LEVELSET test failed: $_"
}

# Test 3: Dependency verification
try {
    $ollamaTest = Test-DependencyReliability -Component "Ollama"
    if ($ollamaTest.Reliable) {
        Write-Host "✅ Ollama dependency reliable"
    } else {
        Write-Host "⚠️  Ollama issues: $($ollamaTest.Errors -join ', ')"
    }
}
catch {
    Write-Host "❌ Dependency test failed: $_"
}

Write-Host "Stabilization test complete. Check !/STATE/ and !/CREWAI/ for logs."