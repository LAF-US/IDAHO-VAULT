# Test script for SimpleStabilization module

# Import module
try {
    Import-Module "$PSScriptRoot\SimpleStabilization.ps1" -Force
    Write-Host "✅ SimpleStabilization module loaded"
}
catch {
    Write-Host "❌ Module load failed: $_"
    exit 1
}

# Test 1: Create stabilization session
try {
    $session = New-StabilizationSession -SessionId "test-001" -InitialContext @{
        Purpose = "System stabilization test"
        Phase = "Initialization"
    }
    
    if ($session.Success) {
        Write-Host "✅ Session created: $($session.SessionFile)"
        
        # Test session update
        $update = Update-StabilizationSession -SessionId "test-001" -Update @{
            EventType = "test_event"
            EventData = @{Message = "Testing session updates"}
        }
        
        if ($update.Success) {
            Write-Host "✅ Session updated successfully"
        } else {
            Write-Host "⚠️  Session update issue: $($update.Error)"
        }
    } else {
        Write-Host "❌ Session creation failed: $($session.Error)"
    }
}
catch {
    Write-Host "❌ Session test failed: $_"
}

# Test 2: Dependency testing
try {
    $ollamaTest = Test-SystemDependency -Component "Ollama"
    Write-Host "Ollama status: $($ollamaTest.Status)"
    if ($ollamaTest.Issues.Count -gt 0) {
        Write-Host "  Issues: $($ollamaTest.Issues -join ', ')"
    }
    
    $openRouterTest = Test-SystemDependency -Component "OpenRouter"
    Write-Host "OpenRouter status: $($openRouterTest.Status)"
    if ($openRouterTest.Issues.Count -gt 0) {
        Write-Host "  Issues: $($openRouterTest.Issues -join ', ')"
    }
}
catch {
    Write-Host "❌ Dependency test failed: $_"
}

# Test 3: LEVELSET compliance
try {
    $levelset = Check-LEVELSETCompliance
    if ($levelset.Compliant) {
        Write-Host "✅ LEVELSET compliance: PASS"
    } else {
        Write-Host "⚠️  LEVELSET compliance: FAIL"
        Write-Host "  Missing: $($levelset.Issues -join ', ')"
    }
}
catch {
    Write-Host "❌ LEVELSET test failed: $_"
}

# Test 4: Error handling
try {
    try {
        throw [System.Exception]::new("Test exception")
    } catch {
        $logResult = Handle-StabilizationError -Error $_ -Context "Test error handling"
        if ($logResult) {
            Write-Host "✅ Error handling: PASS"
        } else {
            Write-Host "⚠️  Error handling: LOGGING FAILED"
        }
    }
}
catch {
    Write-Host "❌ Error handling test failed: $_"
}

Write-Host "Simple stabilization test complete."
Write-Host "Check !/STATE/ and !/CREWAI/ for results."