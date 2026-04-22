function Get-1PasswordPolicy {
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $policyPath = Join-Path $repoRoot ".op\1password-hygiene-policy.json"

    $defaultPolicy = [pscustomobject]@{
        vault_roles = [pscustomobject]@{
            Personal = "consumer-and-general-personal"
            Private  = "segregated-sensitive-personal"
            Vault    = "managed-secrets-and-tooling"
            Wallet   = "financial-and-identity-records"
            Work     = "professional-and-org-accounts"
        }
        managed_service_hints = @(
            "openrouter",
            "anthropic",
            "claude",
            "openai",
            "github",
            "gitlab",
            "linear",
            "vertex",
            "figma",
            "mistral",
            "huggingface",
            "qodo",
            "what3words"
        )
        broad_service_hints = @(
            "google",
            "slack",
            "discord",
            "coinbase",
            "stripe"
        )
        financial_host_patterns = @(
            "creditkarma",
            "venmo",
            "pay\.gov",
            "stlukesbillpay",
            "upstart",
            "personalcapital",
            "freetaxusa",
            "coinbase",
            "stripe",
            "moneylion",
            "moneykey",
            "creditfresh",
            "usbank",
            "bankofamerica",
            "chime",
            "gobank",
            "intuit",
            "turbotax",
            "potlatchno1federalcreditunion"
        )
        impo***REMOVED***tag_patterns = @(
            "^(Imported .+)$",
            "^(CSV Import .+)$",
            "^Starter Kit$"
        )
        idahoptv_patterns = @(
            "@idahoptv\.org\b",
            "\bidahoptv\b"
        )
        personal_email_patterns = @(
            "@gmail\.com\b",
            "@imaxmail\.net\b",
            "@outlook\.com\b",
            "@hotmail\.com\b",
            "@yahoo\.com\b"
        )
        safety_limits = [pscustomobject]@{
            max_moves    = 25
            max_edits    = 100
            max_archives = 25
        }
    }

    if (-not (Test-Path $policyPath)) {
        return $defaultPolicy
    }

    $loaded = Get-Content $policyPath -Raw | ConvertFrom-Json

    foreach ($prop in $defaultPolicy.PSObject.Properties.Name) {
        if (-not ($loaded.PSObject.Properties.Name -contains $prop)) {
            Add-Member -InputObject $loaded -NotePropertyName $prop -NotePropertyValue $defaultPolicy.$prop
        }
    }

    return $loaded
}

function Test-PatternListMatch {
    param(
        [string]$Text,
        [string[]]$Patterns
    )

    if (-not $Text) {
        return $false
    }

    foreach ($pattern in @($Patterns)) {
        if ($Text -match $pattern) {
            return $true
        }
    }

    return $false
}
