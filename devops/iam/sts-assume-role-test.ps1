<#
.SYNOPSIS
    Verification of AWS STS AssumeRole & RBAC on Windows PowerShell.
.PARAMETER RoleArn
    The Amazon Resource Name of the target IAM Role to assume.
#>
param(
    [string]$RoleArn = "arn:aws:iam::123456789012:role/ai-investment-ec2-role-prod"
)

$sessionName = "DevOpsVerificationSession-$((Get-Date).Ticks)"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Testing AWS STS AssumeRole: $RoleArn" -ForegroundColor Cyan
Write-Host "=========================================================="

Write-Host "[1/4] Current IAM Identity:" -ForegroundColor Yellow
aws sts get-caller-identity --output table

Write-Host "`n[2/4] Requesting Temporary STS Credentials..." -ForegroundColor Yellow
$credsJson = aws sts assume-role --role-arn $RoleArn --role-session-name $sessionName --duration-seconds 900 --output json | ConvertFrom-Json

if ($credsJson.Credentials) {
    $env:AWS_ACCESS_KEY_ID = $credsJson.Credentials.AccessKeyId
    $env:AWS_SECRET_ACCESS_KEY = $credsJson.Credentials.SecretAccessKey
    $env:AWS_SESSION_TOKEN = $credsJson.Credentials.SessionToken

    Write-Host "`n[3/4] Assumed Role Identity Verified:" -ForegroundColor Green
    aws sts get-caller-identity --output table

    Write-Host "`n[4/4] Testing RBAC Bucket Access..." -ForegroundColor Yellow
    aws s3 ls
} else {
    Write-Host "Failed to retrieve STS credentials. Verify Role ARN and permissions." -ForegroundColor Red
}
