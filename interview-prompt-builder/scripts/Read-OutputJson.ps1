<#
.SYNOPSIS
Reads and parses an output JSON file created by Write-OutputJson.ps1

.EXAMPLE
.\Read-OutputJson.ps1 -FilePath ".\output.json"

.EXAMPLE
$data = .\Read-OutputJson.ps1 -FilePath ".\output.json"
$data.resolved_inputs
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath
)

function Ensure-Array {
    param($Value)

    if ($null -eq $Value) {
        return @()
    }

    if ($Value -is [System.Array]) {
        return @($Value)
    }

    return @($Value)
}

if (-not (Test-Path $FilePath)) {
    throw "File not found: $FilePath"
}

try {
    $raw = Get-Content -Path $FilePath -Raw | ConvertFrom-Json
}
catch {
    throw "Invalid JSON format in file: $FilePath"
}

$result = [ordered]@{
    resolved_inputs    = Ensure-Array $raw.resolved_inputs
    resolved_outputs   = Ensure-Array $raw.resolved_outputs
    constraints        = Ensure-Array $raw.constraints
    decisions          = Ensure-Array $raw.decisions
    assumptions        = Ensure-Array $raw.assumptions
    codex_personality  = Ensure-Array $raw.codex_personality
    success_criteria   = Ensure-Array $raw.success_criteria
}

# Output as object (best for automation)
$resultObject = New-Object PSObject -Property $result

# Pretty print to console for visibility
Write-Host "`n=== Output JSON Contents ===" -ForegroundColor Cyan

foreach ($key in $result.Keys) {
    Write-Host "`n$key:" -ForegroundColor Yellow
    foreach ($item in $result[$key]) {
        Write-Host "  - $item"
    }
}

# Return object for pipeline use
return $resultObject