<#
LLM Routing and Fallback System
- Prioritizes local Ollama models for cost efficiency
- Uses OpenRouter cloud models as fallback or for specialty cases
- Routes based on request complexity
- Implements cost-aware decision making
#>

# Configuration
$Config = @{
    # Local Ollama Models (sorted by capability/cost)
    LocalModels = @(
        @{Name="gemma4:latest"; Type="light"; MaxTokens=8192; Capability="general"},
        @{Name="llama3.2-vision:90b"; Type="heavy"; MaxTokens=32768; Capability="advanced"}
    )
    
    # OpenRouter Models (sorted by cost - free/cheap first)
    CloudModels = @(
        @{Name="openrouter/auto"; Type="auto"; Cost="free"; Capability="general"},
        @{Name="baidu/cobuddy:free"; Type="light"; Cost="free"; Capability="general"},
        @{Name="mistralai/mistral-7b-instruct:free"; Type="medium"; Cost="free"; Capability="advanced"}
    )
    
    # Complexity thresholds
    ComplexityThresholds = @{
        Simple = 100  # Token estimate for simple requests
        Medium = 500 # Token estimate for medium requests  
        Complex = 2000 # Token estimate for complex requests
    }
}

# Request complexity analyzer
function Analyze-RequestComplexity {
    param(
        [string]$Request
    )
    
    $wordCount = $Request.Split(' ') | Where-Object { $_ -match '\w' } | Measure-Object | Select-Object -ExpandProperty Count
    $tokenEstimate = [math]::Max(1, $wordCount * 1.3) # Rough token estimation
    
    # Determine complexity based on content analysis
    $complexityIndicators = @(
        @{Pattern='code|programming|debug|algorithm'; Weight=3},
        @{Pattern='analyze|compare|explain|detailed'; Weight=2},
        @{Pattern='simple|quick|brief|short'; Weight=0.5}
    )
    
    $complexityScore = 1.0
    foreach ($indicator in $complexityIndicators) {
        if ($Request -match $indicator.Pattern) {
            $complexityScore *= $indicator.Weight
        }
    }
    
    $adjustedTokens = $tokenEstimate * $complexityScore
    
    if ($adjustedTokens -le $Config.ComplexityThresholds.Simple) {
        return @{Level="simple"; Tokens=$adjustedTokens; ModelType="light"}
    } elseif ($adjustedTokens -le $Config.ComplexityThresholds.Medium) {
        return @{Level="medium"; Tokens=$adjustedTokens; ModelType="medium"}
    } else {
        return @{Level="complex"; Tokens=$adjustedTokens; ModelType="heavy"}
    }
}

# Model selector with fallback logic
function Select-LLMModel {
    param(
        [string]$Request,
        [string]$RequiredCapability = "general",
        [bool]$ForceCloud = $false
    )
    
    $analysis = Analyze-RequestComplexity -Request $Request
    Write-Host "Request Analysis: Complexity=$($analysis.Level), EstimatedTokens=$($analysis.Tokens), ModelType=$($analysis.ModelType)"
    
    # Try local models first (unless cloud is forced)
    if (-not $ForceCloud) {
        $localCandidates = $Config.LocalModels | Where-Object {
            ($_.Capability -eq $RequiredCapability -or $_.Capability -eq "general") -and
            ($_.Type -eq $analysis.ModelType -or $analysis.ModelType -eq "light" -and $_.Type -eq "medium")
        } | Sort-Object @{Expression={if ($_.Type -eq "light") {0} elseif ($_.Type -eq "medium") {1} else {2}}}
        
        if ($localCandidates) {
            $selected = $localCandidates | Select-Object -First 1
            Write-Host "Selected Local Model: $($selected.Name) (Type: $($selected.Type), Capability: $($selected.Capability))"
            return @{
                Provider="ollama";
                Model=$selected.Name;
                Type=$selected.Type;
                Reason="Local model available and suitable"
            }
        }
    }
    
    # Fallback to cloud models
    $cloudCandidates = $Config.CloudModels | Where-Object {
        ($_.Capability -eq $RequiredCapability -or $_.Capability -eq "general") -and
        ($_.Type -eq $analysis.ModelType -or $analysis.ModelType -eq "light" -and $_.Type -eq "medium")
    } | Sort-Object @{Expression={if ($_.Cost -eq "free") {0} else {1}}, @{Expression={if ($_.Type -eq "light") {0} elseif ($_.Type -eq "medium") {1} else {2}}}
    
    if ($cloudCandidates) {
        $selected = $cloudCandidates | Select-Object -First 1
        Write-Host "Selected Cloud Model: $($selected.Name) (Type: $($selected.Type), Cost: $($selected.Cost))"
        return @{
            Provider="openrouter";
            Model=$selected.Name;
            Type=$selected.Type;
            Reason="Cloud fallback - $($selected.Cost) tier"
        }
    }
    
    throw "No suitable model found for this request"
}

# Execute LLM request with selected model
function Invoke-LLMRequest {
    param(
        [string]$Request,
        [string]$RequiredCapability = "general",
        [bool]$ForceCloud = $false
    )
    
    try {
        $modelSelection = Select-LLMModel -Request $Request -RequiredCapability $RequiredCapability -ForceCloud $ForceCloud
        
        if ($modelSelection.Provider -eq "ollama") {
            Write-Host "Executing with Ollama..."
            $result = ollama run $modelSelection.Model $Request
            return @{
                Success=$true;
                Result=$result;
                Model=$modelSelection.Model;
                Provider="ollama";
                Cost="free"
            }
        } elseif ($modelSelection.Provider -eq "openrouter") {
            Write-Host "Executing with OpenRouter..."
            # Note: This would need actual OpenRouter API call implementation
            # For now, we'll simulate the response
            $simulatedResult = "OpenRouter response for model $($modelSelection.Model)"
            return @{
                Success=$true;
                Result=$simulatedResult;
                Model=$modelSelection.Model;
                Provider="openrouter";
                Cost=$Config.CloudModels | Where-Object { $_.Name -eq $modelSelection.Model } | Select-Object -ExpandProperty Cost
            }
        }
    } catch {
        return @{
            Success=$false;
            Error=$_.Exception.Message;
            Provider="error"
        }
    }
}

# Example usage
Write-Host "=== LLM Routing System Test ==="

# Test 1: Simple request (should use local light model)
Write-Host "`nTest 1: Simple request"
$result1 = Invoke-LLMRequest -Request "What's the weather like today?"
Write-Host "Result: $($result1.Provider) - $($result1.Model) - Cost: $($result1.Cost)"

# Test 2: Complex request (should use local heavy model if available)
Write-Host "`nTest 2: Complex request"
$result2 = Invoke-LLMRequest -Request "Explain how quantum computing works and provide code examples in Python"
Write-Host "Result: $($result2.Provider) - $($result2.Model) - Cost: $($result2.Cost)"

# Test 3: Specialty request requiring cloud (force cloud)
Write-Host "`nTest 3: Specialty request (force cloud)"
$result3 = Invoke-LLMRequest -Request "Analyze this complex financial data" -ForceCloud $true
Write-Host "Result: $($result3.Provider) - $($result3.Model) - Cost: $($result3.Cost)"

Write-Host "`n=== Routing System Ready ==="