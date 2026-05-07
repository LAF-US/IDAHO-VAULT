<#
.VAULT STABILIZATION MODULE
Governance: CONSTITUTION.md § I, § III
Protocol: LEVELSET-compliant
State Management: !/STATE/
Error Logging: !/CREWAI/
#>

# Module initialization
$script:ModuleBasePath = $PSScriptRoot
$script:VaultRoot = Split-Path $PSScriptRoot -Parent

# Import common utilities if available
try {
    $commonModule = Join-Path $script:VaultRoot "scripts-vault-common.ps1"
    if (Test-Path $commonModule) {
        . $commonModule
    }
}
catch {
    Write-Verbose "Vault common utilities unavailable - running in standalone mode"
}

# State management functions
function Initialize-StateSession {
    <#
    .SYNOPSIS
        Creates a new state session with governance compliance
    .DESCRIPTION
        Initializes a state session in !/STATE/ with proper metadata
    .PARAMETER SessionId
        Unique identifier for this session
    .PARAMETER Context
        Initial context data for the session
    .EXAMPLE
        $session = Initialize-StateSession -SessionId "llm-router-001"
    .GOVERNANCE
        Authority: CONSTITUTION.md § I.4
        Location: !/STATE/
        Logging: !/CREWAI/state-log.jsonl
    #>
    
    param(
        [Parameter(Mandatory=$true)]
        [string]$SessionId,
        
        [hashtable]$Context = @{}
    )
    
    try {
        # Ensure state directory exists
        $stateDir = Join-Path $script:VaultRoot "!" "STATE"
        if (-not (Test-Path $stateDir)) {
            New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
        }
        
        # Create state file
        $stateFile = Join-Path $stateDir "$SessionId.json"
        
        $state = @{
            SessionId = $SessionId
            Timestamp = Get-Date -Format "o"
            Status = "initialized"
            Context = $Context
            History = @()
            Governance = @{
                Authority = "CONSTITUTION.md"
                Protocol = "LEVELSET"
                Compliance = "NETWEB/MESHWEB"
            }
        }
        
        # Write state file
        $state | ConvertTo-Json -Depth 10 | Out-File $stateFile -Force
        
        # Log initialization
        Log-StateEvent -SessionId $SessionId -EventType "initialized"
        
        return @{
            Success = $true
            StateFile = $stateFile
            State = $state
        }
    }
    catch {
        $errorLog = @{
            Timestamp = Get-Date -Format "o"
            SessionId = $SessionId
            Error = $_.Exception.Message
            StackTrace = $_.Exception.StackTrace
            Status = "initialization_failed"
        }
        
        Log-StateEvent -SessionId $SessionId -EventType "initialization_failed" -Error $errorLog
        
        return @{
            Success = $false
            Error = $errorLog
        }
    }
}

function Update-StateSession {
    <#
    .SYNOPSIS
        Updates an existing state session
    .DESCRIPTION
        Appends to session history and updates context
    .PARAMETER SessionId
        Existing session identifier
    .PARAMETER Update
        Update data to add to state
    .GOVERNANCE
        Authority: CONSTITUTION.md § I.4
        Location: !/STATE/
    #>
    
    param(
        [Parameter(Mandatory=$true)]
        [string]$SessionId,
        
        [hashtable]$Update
    )
    
    try {
        $stateFile = Join-Path $script:VaultRoot "!" "STATE" "$SessionId.json"
        
        if (-not (Test-Path $stateFile)) {
            throw "State session $SessionId not found"
        }
        
        $currentState = Get-Content $stateFile | ConvertFrom-Json
        
        # Update state
        if ($Update.Context) {
            $currentState.Context = $Update.Context
        }
        
        if ($Update.Status) {
            $currentState.Status = $Update.Status
        }
        
        # Add to history
        $historyEntry = @{
            Timestamp = Get-Date -Format "o"
            Action = $Update.Action
            Data = $Update.Data
        }
        
        $currentState.History += $historyEntry
        
        # Save updated state
        $currentState | ConvertTo-Json -Depth 10 | Out-File $stateFile -Force
        
        Log-StateEvent -SessionId $SessionId -EventType "updated" -Data $Update
        
        return @{
            Success = $true
            State = $currentState
        }
    }
    catch {
        Log-StateEvent -SessionId $SessionId -EventType "update_failed" -Error $_
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

function Get-StateSession {
    <#
    .SYNOPSIS
        Retrieves an existing state session
    .PARAMETER SessionId
        Session identifier to retrieve
    .GOVERNANCE
        Authority: CONSTITUTION.md § I.4
        Location: !/STATE/
    #>
    
    param(
        [Parameter(Mandatory=$true)]
        [string]$SessionId
    )
    
    try {
        $stateFile = Join-Path $script:VaultRoot "!" "STATE" "$SessionId.json"
        
        if (-not (Test-Path $stateFile)) {
            return @{
                Success = $false
                Error = "State session $SessionId not found"
            }
        }
        
        $state = Get-Content $stateFile | ConvertFrom-Json
        return @{
            Success = $true
            State = $state
        }
    }
    catch {
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

# Dependency verification functions
function Test-DependencyReliability {
    <#
    .SYNOPSIS
        Verifies reliability of system dependencies
    .DESCRIPTION
        Tests components before relying on them
    .PARAMETER Component
        Component name to test
    .GOVERNANCE
        Authority: CONSTITUTION.md § I.1
        Protocol: LEVELSET pre-flight
    #>
    
    param(
        [Parameter(Mandatory=$true)]
        [string]$Component
    )
    
    $result = @{
        Component = $Component
        Timestamp = Get-Date -Format "o"
        Tests = @()
        Warnings = @()
        Errors = @()
        Reliable = $null
    }
    
    try {
        switch ($Component) {
            "OpenRouter" {
                $result.Tests += "Connection test"
                try {
                    # Test OpenRouter API connectivity
                    $apiTest = Invoke-RestMethod -Uri "https://openrouter.ai/api/v1/models" -Headers @{"Authorization"="Bearer test"} -Method Get -ErrorAction Stop
                    $result.Tests += "API test passed"
                    $result.Reliable = $true
                }
                catch {
                    $result.Errors += "API test failed: $($_)"
                    $result.Reliable = $false
                }
            }
            
            "Ollama" {
                $result.Tests += "Service availability"
                try {
                    $ollamaCommand = Get-Command ollama -ErrorAction SilentlyContinue
                    if (-not $ollamaCommand) {
                        throw "ollama executable not found"
                    }

                    $serviceTest = & $ollamaCommand.Source ps 2>&1
                    if ($LASTEXITCODE -ne 0) {
                        throw ($serviceTest -join "`n")
                    }

                    if ($serviceTest -match "gemma4:latest") {
                        $result.Tests += "Model availability confirmed"
                        $result.Reliable = $true
                    }
                    else {
                        $result.Warnings += "Ollama running but expected models not found"
                        $result.Reliable = $false
                    }
                }
                catch {
                    $result.Errors += "Ollama service test failed: $($_)"
                    $result.Reliable = $false
                }
            }
            
            "1Password" {
                $result.Tests += "CLI availability"
                if (Test-CommandAvailable "op") {
                    $result.Tests += "CLI available"
                    try {
                        $whoami = op whoami -ErrorAction Stop
                        $result.Tests += "Authentication verified"
                        $result.Reliable = $true
                    }
                    catch {
                        $result.Errors += "Authentication failed: $($_)"
                        $result.Reliable = $false
                    }
                }
                else {
                    $result.Errors += "1Password CLI not available"
                    $result.Reliable = $false
                }
            }
            
            default {
                $result.Warnings += "Unknown component: $Component"
                $result.Reliable = $null
            }
        }
    }
    catch {
        $result.Errors += "Test execution failed: $($_)"
        $result.Reliable = $false
    }
    
    # Log test results
    Log-DependencyTest $result
    
    return $result
}

# Error handling functions
function Handle-AgentError {
    <#
    .SYNOPSIS
        Governance-compliant error handling
    .DESCRIPTION
        Logs errors and attempts recovery
    .PARAMETER Error
        Exception object to handle
    .PARAMETER Context
        Contextual information about the error
    .GOVERNANCE
        Authority: CONSTITUTION.md § I.4
        Location: !/CREWAI/errors.jsonl
    #>
    
    param(
        [Parameter(Mandatory=$true)]
        [Exception]$Error,
        
        [hashtable]$Context = @{}
    )
    
    # Create comprehensive error log
    $errorLog = @{
        Timestamp = Get-Date -Format "o"
        ErrorType = $Error.GetType().FullName
        Message = $Error.Message
        Context = $Context
        StackTrace = $Error.StackTrace
        Severity = "critical"
        RecoveryAction = "manual_intervention_required"
    }
    
    # Write to governance-approved location
    try {
        $logDir = Join-Path $script:VaultRoot "!" "CREWAI"
        if (-not (Test-Path $logDir)) {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        
        $logFile = Join-Path $logDir "errors.jsonl"
        $errorLog | ConvertTo-Json -Depth 10 | Out-File $logFile -Append
        
        # Attempt recovery if possible
        $recovery = Attempt-ErrorRecovery $Error $Context
        if ($recovery.Success) {
            $errorLog.RecoveryAction = "automatic_recovery_successful"
            $errorLog.RecoveryDetails = $recovery.Details
        }
        
        return @{
            Success = $true
            ErrorLog = $errorLog
            Recovery = $recovery
        }
    }
    catch {
        # Final fallback - write to console if logging fails
        Write-Error "CRITICAL: Error logging failed - $($_)"
        Write-Error "Original error: $($Error.Message)"
        
        return @{
            Success = $false
            Error = "Logging system failure"
            OriginalError = $Error
        }
    }
}

function Attempt-ErrorRecovery {
    <#
    .SYNOPSIS
        Attempts automatic recovery from errors
    .DESCRIPTION
        Implements recovery strategies for known error patterns
    #>
    
    param(
        [Exception]$Error,
        [hashtable]$Context
    )
    
    $recoveryAttempt = @{
        Success = $false
        Strategy = "none"
        Details = @{}
    }
    
    # Known recovery patterns
    if ($Error.Message -match "connection refused") {
        $recoveryAttempt.Strategy = "retry_with_backoff"
        $recoveryAttempt.Details = @{
            Attempts = 3
            DelayMs = 1000
            Result = "not_implemented"
        }
    }
    elseif ($Error.Message -match "authentication failed") {
        $recoveryAttempt.Strategy = "refresh_credentials"
        $recoveryAttempt.Details = @{
            Method = "op_refresh"
            Result = "not_implemented"
        }
    }
    elseif ($Error.Message -match "model not found") {
        $recoveryAttempt.Strategy = "fallback_model"
        $recoveryAttempt.Details = @{
            Fallback = "gemma4:latest"
            Result = "not_implemented"
        }
    }
    
    return $recoveryAttempt
}

# Logging functions
function Log-StateEvent {
    <#
    .SYNOPSIS
        Logs state management events
    .GOVERNANCE
        Authority: CONSTITUTION.md § I.4
        Location: !/CREWAI/state-log.jsonl
    #>
    
    param(
        [string]$SessionId,
        [string]$EventType,
        [hashtable]$Data = @{},
        [hashtable]$Error = @{}
    )
    
    $logEntry = @{
        Timestamp = Get-Date -Format "o"
        SessionId = $SessionId
        EventType = $EventType
        Data = $Data
        Error = $Error
    }
    
    try {
        $logDir = Join-Path $script:VaultRoot "!" "CREWAI"
        if (-not (Test-Path $logDir)) {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        
        $logFile = Join-Path $logDir "state-log.jsonl"
        $logEntry | ConvertTo-Json -Depth 10 | Out-File $logFile -Append -ErrorAction SilentlyContinue
        return $true
    }
    catch {
        Write-Warning "State logging failed: $($_)"
        return $false
    }
}

function Log-DependencyTest {
    <#
    .SYNOPSIS
        Logs dependency verification results
    .GOVERNANCE
        Authority: CONSTITUTION.md § I.4
        Location: !/CREWAI/dependency-log.jsonl
    #>
    
    param(
        [hashtable]$TestResult
    )
    
    try {
        $logDir = Join-Path $script:VaultRoot "!" "CREWAI"
        if (-not (Test-Path $logDir)) {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        
        $logFile = Join-Path $logDir "dependency-log.jsonl"
        $TestResult | ConvertTo-Json -Depth 10 | Out-File $logFile -Append -ErrorAction SilentlyContinue
        return $true
    }
    catch {
        Write-Warning "Dependency logging failed: $($_)"
        return $false
    }
}

# LEVELSET protocol compliance
function Perform-LEVELSETCheck {
    <#
    .SYNOPSIS
        Performs LEVELSET protocol compliance check
    .DESCRIPTION
        Verifies system state before operations
    .GOVERNANCE
        Authority: CONSTITUTION.md § III
        Protocol: LEVELSET-STEP-0-EXTERNAL-AGENT.md
    #>
    
    $bangRoot = Join-Path $script:VaultRoot "!"

    $checkResults = @{
        Timestamp = Get-Date -Format "o"
        Governance = @{
            Constitution = Test-Path (Join-Path $script:VaultRoot "CONSTITUTION.md")
            Levelset = Test-Path (Join-Path $script:VaultRoot "LEVELSET.md")
            Agents = Test-Path (Join-Path $script:VaultRoot "AGENTS.md")
        }
        Infrastructure = @{
            StateDirectory = Test-Path (Join-Path $bangRoot "STATE")
            CrevaiDirectory = Test-Path (Join-Path $bangRoot "CREWAI")
        }
        Valid = $true
        Issues = @()
    }
    
    # Check governance files
    foreach ($govCheck in $checkResults.Governance.Keys) {
        if (-not $checkResults.Governance.$govCheck) {
            $checkResults.Valid = $false
            $checkResults.Issues += "Missing governance file: $govCheck"
        }
    }
    
    # Check infrastructure
    foreach ($infCheck in $checkResults.Infrastructure.Keys) {
        if (-not $checkResults.Infrastructure.$infCheck) {
            $checkResults.Issues += "Missing infrastructure: $infCheck"
        }
    }
    
    # Log LEVELSET check
    Log-LEVELSETCheck $checkResults
    
    return $checkResults
}

function Log-LEVELSETCheck {
    <#
    .SYNOPSIS
        Logs LEVELSET compliance checks
    .GOVERNANCE
        Authority: CONSTITUTION.md § I.4
        Location: !/CREWAI/levelset-log.jsonl
    #>
    
    param([hashtable]$CheckResult)
    
    try {
        $logDir = Join-Path $script:VaultRoot "!" "CREWAI"
        if (-not (Test-Path $logDir)) {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        
        $logFile = Join-Path $logDir "levelset-log.jsonl"
        $CheckResult | ConvertTo-Json -Depth 10 | Out-File $logFile -Append -ErrorAction SilentlyContinue
        return $true
    }
    catch {
        Write-Warning "LEVELSET logging failed: $($_)"
        return $false
    }
}

# Export module members
Export-ModuleMember -Function @(
    'Initialize-StateSession',
    'Update-StateSession',
    'Get-StateSession',
    'Test-DependencyReliability',
    'Handle-AgentError',
    'Perform-LEVELSETCheck',
    'Log-StateEvent',
    'Log-DependencyTest'
)

# Module footer
<#
.MODULE FOOTER
This stabilization module implements CONSTITUTION.md-compliant state management
and error handling for the IDAHO-VAULT agentic swarm system.

Governance: CONSTITUTION.md § I, § III
Protocol: LEVELSET-compliant
State: !/STATE/
Logs: !/CREWAI/

"The world is quiet here. Esto Perpetua."
#>
