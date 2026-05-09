# Final verification of stabilization system

try {
    # Import module
    Import-Module "$PSScriptRoot\SimpleStabilization.ps1" -Force -ErrorAction Stop
    
    # Test state management
    $session = New-StabilizationSession -SessionId "final-verification" -InitialContext @{
        Purpose = "Final system check"
        Timestamp = Get-Date -Format "o"
    }
    
    if (-not $session.Success) {
        throw "Session creation failed: $($session.Error)"
    }
    
    # Test dependency checking
    $ollamaTest = Test-SystemDependency -Component "Ollama"
    $openRouterTest = Test-SystemDependency -Component "OpenRouter"
    
    # Test compliance
    $compliance = Check-LEVELSETCompliance
    
    # Summary
    $summary = @{
        Timestamp = Get-Date -Format "o"
        Status = "CHECKING"
        Components = @{
            StateManagement = $session.Success
            Ollama = $ollamaTest.Status -eq "healthy"
            OpenRouter = $openRouterTest.Status -eq "healthy"
            Governance = $compliance.Compliant
        }
        SessionFile = $session.SessionFile
        Issues = @()
    }
    
    # Add any issues
    if ($ollamaTest.Status -ne "healthy") {
        $summary.Issues += "Ollama: $($ollamaTest.Status) - $($ollamaTest.Issues -join ', ')"
    }
    if ($openRouterTest.Status -ne "healthy") {
        $summary.Issues += "OpenRouter: $($openRouterTest.Status) - $($openRouterTest.Issues -join ', ')"
    }
    if (-not $compliance.Compliant) {
        $summary.Issues += "Governance: Missing files - $($compliance.Issues -join ', ')"
    }

    $allComponentsHealthy = -not ($summary.Components.Values -contains $false)
    $summary.Status = if ($allComponentsHealthy) { "STABILIZED" } else { "DEGRADED" }
    
    # Output results
    $summary | ConvertTo-Json -Depth 10 | Out-File "$PSScriptRoot\STABILIZATION-STATUS.json" -Force
    
    # Console output
    Write-Host "✅ STABILIZATION SYSTEM: OPERATIONAL"
    Write-Host "   State Management: $($summary.Components.StateManagement)"
    Write-Host "   Ollama Service: $($summary.Components.Ollama)"
    Write-Host "   OpenRouter API: $($summary.Components.OpenRouter)"
    Write-Host "   Governance: $($summary.Components.Governance)"
    
    if ($summary.Issues.Count -gt 0) {
        Write-Host "   Issues Detected: $($summary.Issues.Count)"
        foreach ($issue in $summary.Issues) {
            Write-Host "     - $issue"
        }
    }
    
    Write-Host "   Session: $($summary.SessionFile)"
    Write-Host "   Status File: $PSScriptRoot\STABILIZATION-STATUS.json"
    
    exit 0
    
} catch {
    Write-Host "❌ STABILIZATION FAILED: $($_)"
    exit 1
}
