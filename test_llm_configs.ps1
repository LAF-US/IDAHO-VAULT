# Test script to verify Ollama and OpenRouter configurations

# Test Ollama
Write-Host "Testing Ollama..."
$ollamaOutput = ollama run gemma4 "Test Ollama configuration" 2>&1
if ($ollamaOutput -match "Test Ollama configuration") {
    Write-Host "✓ Ollama is working correctly"
} else {
    Write-Host "✗ Ollama test failed"
}

# Test OpenRouter
Write-Host "Testing OpenRouter..."
$openRouterOutput = Invoke-RestMethod -Uri "https://openrouter.ai/api/v1/models" -Headers @{"Authorization"="Bearer $OPENROUTER_API_KEY"} -ErrorAction SilentlyContinue
if ($openRouterOutput -and $openRouterOutput.data -and $openRouterOutput.data.Count -gt 0) {
    Write-Host "✓ OpenRouter is working correctly"
    Write-Host "Available models: $($openRouterOutput.data.Count)"
} else {
    Write-Host "✗ OpenRouter test failed"
}

Write-Host "Configuration verification complete!"