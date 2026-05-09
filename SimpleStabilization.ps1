<#
SIMPLE STABILIZATION SYSTEM
Governance: CONSTITUTION.md § I, § III
Protocol: LEVELSET-compliant
Purpose: Provide basic state management and error handling
#>

# Basic state management
function New-StabilizationSession {
    param(
        [string]$SessionId = "auto-$(Get-Date -Format "yyyyMMdd-HHmmss")",
        [hashtable]$InitialContext = @{}
    )
    
    # Create state directory if needed
    $stateDir = "$PSScriptRoot\!\STATE"
    if (-not (Test-Path $stateDir)) {
        New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
    }

    # Create log directory if needed
    $logDir = "$PSScriptRoot\!\CREWAI"
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    # Create session file
    $sessionFile = Join-Path $stateDir "$SessionId.json"
    
    $session = @{
        SessionId = $SessionId
        Created = Get-Date -Format "o"
        Status = "active"
        Context = $InitialContext
        Events = @()
    }
    
    try {
        $session | ConvertTo-Json -Depth 10 | Out-File $sessionFile -Force
        return @{
            Success = $true
            SessionFile = $sessionFile
            Session = $session
        }
    }
    catch {
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

function Update-StabilizationSession {
    param(
        [string]$SessionId,
        [hashtable]$Update
    )
    
    $sessionFile = "$PSScriptRoot\!\STATE\$SessionId.json"
    
    if (-not (Test-Path $sessionFile)) {
        return @{
            Success = $false
            Error = "Session $SessionId not found"
        }
    }
    
    try {
        $session = Get-Content $sessionFile | ConvertFrom-Json
        
        # Update session
        if ($Update.Status) { $session.Status = $Update.Status }
        if ($Update.Context) { $session.Context = $Update.Context }
        
        # Add event
        $event = @{
            Timestamp = Get-Date -Format "o"
            Type = $Update.EventType
            Data = $Update.EventData
        }
        $session.Events += $event
        
        # Save
        $session | ConvertTo-Json -Depth 10 | Out-File $sessionFile -Force
        
        return @{
            Success = $true
            Session = $session
        }
    }
    catch {
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

# Simple dependency testing
function Test-SystemDependency {
    param([string]$Component)
    
    $result = @{Component=$Component; Status="untested"; Issues=@()}
    
    try {
        switch ($Component) {
            "Ollama" {
                try {
                    $ollamaCommand = Get-Command ollama -ErrorAction SilentlyContinue
                    if (-not $ollamaCommand) {
                        throw "ollama executable not found"
                    }

                    $ollamaTest = & $ollamaCommand.Source ps 2>&1
                    if ($LASTEXITCODE -ne 0) {
                        throw ($ollamaTest -join "`n")
                    }

                    if ($ollamaTest -match "gemma4:latest") {
                        $result.Status = "healthy"
                    } else {
                        $result.Status = "degraded"
                        $result.Issues += "Expected models not running"
                    }
                } catch {
                    $result.Status = "failed"
                    $result.Issues += "Service unavailable: $($_)"
                }
            }
            
            "OpenRouter" {
                try {
                    # Basic connectivity test
                    $null = Invoke-WebRequest -Uri "https://openrouter.ai" -Method Head -ErrorAction Stop
                    $result.Status = "healthy"
                } catch {
                    $result.Status = "failed"
                    $result.Issues += "Connectivity failed: $($_)"
                }
            }
            
            default {
                $result.Status = "unknown"
                $result.Issues += "Component test not implemented"
            }
        }
    } catch {
        $result.Status = "error"
        $result.Issues += "Test failed: $($_)"
    }
    
    return $result
}

# Basic error handling
function Handle-StabilizationError {
    param(
        [Exception]$Error,
        [string]$Context = "unknown"
    )
    
    $errorLog = @{
        Timestamp = Get-Date -Format "o"
        Context = $Context
        Type = $Error.GetType().FullName
        Message = $Error.Message
        StackTrace = $Error.StackTrace
    }
    
    try {
        $logDir = "$PSScriptRoot\!\CREWAI"
        if (-not (Test-Path $logDir)) {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        
        $logFile = Join-Path $logDir "errors.jsonl"
        $errorLog | ConvertTo-Json -Depth 10 | Out-File $logFile -Append
        return $true
    } catch {
        Write-Warning "Error logging failed: $($_)"
        return $false
    }
}

# Simple LEVELSET check
function Check-LEVELSETCompliance {
    $vaultRoot = (Resolve-Path $PSScriptRoot).Path
    $bangRoot = Join-Path $vaultRoot "!"

    $checks = @{
        Constitution = Test-Path (Join-Path $vaultRoot "CONSTITUTION.md")
        Levelset = Test-Path (Join-Path $vaultRoot "LEVELSET.md")
        Agents = Test-Path (Join-Path $vaultRoot "AGENTS.md")
        StateDir = Test-Path (Join-Path $bangRoot "STATE")
        CrevaiDir = Test-Path (Join-Path $bangRoot "CREWAI")
    }
    
    $compliant = $true
    $issues = @()
    
    foreach ($check in $checks.Keys) {
        if (-not $checks.$check) {
            $compliant = $false
            $issues += $check
        }
    }
    
    return @{
        Compliant = $compliant
        Checks = $checks
        Issues = $issues
    }
}

# Make functions available without Export-ModuleMember
# (Since this is a script file, not a proper module)
Set-Alias -Name New-StabSession -Value New-StabilizationSession -Scope Global
Set-Alias -Name Update-StabSession -Value Update-StabilizationSession -Scope Global
Set-Alias -Name Test-Dependency -Value Test-SystemDependency -Scope Global
Set-Alias -Name Handle-StabError -Value Handle-StabilizationError -Scope Global
Set-Alias -Name Check-LEVELSET -Value Check-LEVELSETCompliance -Scope Global

Write-Verbose "SimpleStabilization functions loaded (using aliases)"
