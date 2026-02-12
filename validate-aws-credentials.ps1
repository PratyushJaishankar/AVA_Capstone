# AWS Credentials Validator for GitHub Secrets
# This script helps you validate your AWS credentials before adding them to GitHub

Write-Host "=== AWS Credentials Validator ===" -ForegroundColor Cyan
Write-Host ""

# Function to validate and clean input
function Validate-AWSCredential {
    param(
        [string]$Name,
        [string]$Value,
        [int]$ExpectedLength,
        [string]$Pattern = ""
    )

    Write-Host "Checking $Name..." -ForegroundColor Yellow

    # Trim whitespace
    $CleanValue = $Value.Trim()

    # Check length
    $ActualLength = $CleanValue.Length
    Write-Host "  Length: $ActualLength characters (expected: $ExpectedLength)" -ForegroundColor Gray

    if ($ActualLength -ne $ExpectedLength) {
        Write-Host "  ❌ INVALID: Length mismatch!" -ForegroundColor Red
        Write-Host "     Has extra spaces or wrong value" -ForegroundColor Red
        return $false
    }

    # Check pattern if provided
    if ($Pattern -and $CleanValue -notmatch $Pattern) {
        Write-Host "  ❌ INVALID: Format doesn't match expected pattern!" -ForegroundColor Red
        return $false
    }

    Write-Host "  ✅ Valid format" -ForegroundColor Green
    Write-Host "  Clean value: $CleanValue" -ForegroundColor Gray
    return $true
}

Write-Host "Please paste your AWS credentials (they will be validated):" -ForegroundColor Cyan
Write-Host ""

# Get AWS Access Key ID
Write-Host "1. AWS Access Key ID (should be 20 characters starting with AKIA):" -ForegroundColor White
$AccessKeyId = Read-Host "   Paste here"

# Get AWS Secret Access Key
Write-Host ""
Write-Host "2. AWS Secret Access Key (should be 40 characters):" -ForegroundColor White
$SecretAccessKey = Read-Host "   Paste here" -AsSecureString
$SecretAccessKeyPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecretAccessKey)
)

# Get AWS Region
Write-Host ""
Write-Host "3. AWS Region (e.g., us-east-1, us-west-2, ap-south-1):" -ForegroundColor White
$Region = Read-Host "   Enter region"

Write-Host ""
Write-Host "=== Validation Results ===" -ForegroundColor Cyan
Write-Host ""

# Validate each credential
$AccessKeyValid = Validate-AWSCredential -Name "AWS_ACCESS_KEY_ID" -Value $AccessKeyId -ExpectedLength 20 -Pattern "^AKIA"
$SecretKeyValid = Validate-AWSCredential -Name "AWS_SECRET_ACCESS_KEY" -Value $SecretAccessKeyPlain -ExpectedLength 40
$RegionValid = $Region.Trim().Length -gt 0

Write-Host ""
if ($RegionValid) {
    $CleanRegion = $Region.Trim()
    Write-Host "AWS_REGION: $CleanRegion" -ForegroundColor Green

    # Validate region format
    $ValidRegions = @('us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1')
    if ($CleanRegion -notin $ValidRegions) {
        Write-Host "  ⚠️  Warning: This doesn't look like a standard AWS region" -ForegroundColor Yellow
        Write-Host "     Common regions: us-east-1, us-west-2, eu-west-1, ap-south-1" -ForegroundColor Yellow
    } else {
        Write-Host "  ✅ Valid AWS region" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan

if ($AccessKeyValid -and $SecretKeyValid -and $RegionValid) {
    Write-Host "✅ All credentials appear valid!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Copy these EXACT values to GitHub Secrets:" -ForegroundColor White
    Write-Host ""
    Write-Host "AWS_ACCESS_KEY_ID:" -ForegroundColor Yellow
    Write-Host "$($AccessKeyId.Trim())" -ForegroundColor White
    Write-Host ""
    Write-Host "AWS_SECRET_ACCESS_KEY:" -ForegroundColor Yellow
    Write-Host "$($SecretAccessKeyPlain.Trim())" -ForegroundColor White
    Write-Host ""
    Write-Host "AWS_REGION:" -ForegroundColor Yellow
    Write-Host "$($Region.Trim())" -ForegroundColor White
    Write-Host ""
    Write-Host "⚠️  When pasting to GitHub:" -ForegroundColor Yellow
    Write-Host "   1. Copy each value above" -ForegroundColor Gray
    Write-Host "   2. Go to: Settings → Secrets and variables → Actions → Secrets" -ForegroundColor Gray
    Write-Host "   3. Delete old secrets if they exist" -ForegroundColor Gray
    Write-Host "   4. Create new secrets with exact values above" -ForegroundColor Gray
    Write-Host "   5. Do NOT add extra spaces or newlines" -ForegroundColor Gray
} else {
    Write-Host "❌ Some credentials are invalid. Please check:" -ForegroundColor Red
    Write-Host ""
    if (-not $AccessKeyValid) {
        Write-Host "  • AWS_ACCESS_KEY_ID must be exactly 20 characters" -ForegroundColor Red
        Write-Host "    It should start with 'AKIA'" -ForegroundColor Red
        Write-Host "    Your value: '$AccessKeyId' (length: $($AccessKeyId.Length))" -ForegroundColor Gray
    }
    if (-not $SecretKeyValid) {
        Write-Host "  • AWS_SECRET_ACCESS_KEY must be exactly 40 characters" -ForegroundColor Red
        Write-Host "    Your value length: $($SecretAccessKeyPlain.Length)" -ForegroundColor Gray
    }
    if (-not $RegionValid) {
        Write-Host "  • AWS_REGION cannot be empty" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Get correct values from AWS Console:" -ForegroundColor Yellow
    Write-Host "  IAM → Users → Your User → Security Credentials → Access Keys" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
