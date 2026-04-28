param(
    [string]$SpecPath,
    [string]$PlanPath,
    [string]$SpecText,
    [string]$PlanText
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-StringHash {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Value)
        $hashBytes = $sha.ComputeHash($bytes)
        return ([System.BitConverter]::ToString($hashBytes)).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Resolve-InputText {
    param(
        [string]$PathValue,
        [string]$TextValue,
        [string]$Label
    )

    if ($PSBoundParameters.ContainsKey("TextValue") -and $null -ne $TextValue -and $TextValue -ne "") {
        return $TextValue
    }

    if ($PSBoundParameters.ContainsKey("PathValue") -and $null -ne $PathValue -and $PathValue -ne "") {
        $resolved = Resolve-Path -LiteralPath $PathValue
        return [System.IO.File]::ReadAllText($resolved.Path, [System.Text.Encoding]::UTF8)
    }

    throw "Missing input for $Label. Provide either the text value or a file path."
}

$specContent = Resolve-InputText -PathValue $SpecPath -TextValue $SpecText -Label "specification"
$planContent = Resolve-InputText -PathValue $PlanPath -TextValue $PlanText -Label "execution plan"

$result = [ordered]@{
    source_spec_hash = Get-StringHash -Value $specContent
    execution_plan_hash = Get-StringHash -Value $planContent
}

$result | ConvertTo-Json -Compress
