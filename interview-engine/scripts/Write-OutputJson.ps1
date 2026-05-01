<#
.SYNOPSIS
Creates or overwrites a JSON file with output structure fields.

.EXAMPLE
.\Write-OutputJson.ps1 `
  -FilePath ".\output.json" `
  -ResolvedInputs @("input1") `
  -ResolvedOutputs @("output1") `
  -Constraints @("constraint1") `
  -Decisions @("decision1") `
  -Assumptions @("assumption1") `
  -CodexPersonality @("structured","direct") `
  -SuccessCriteria @("valid json")
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,

    [string[]]$ResolvedInputs = @(),
    [string[]]$ResolvedOutputs = @(),
    [string[]]$Constraints = @(),
    [string[]]$Decisions = @(),
    [string[]]$Assumptions = @(),
    [string[]]$CodexPersonality = @(),
    [string[]]$SuccessCriteria = @()
)

$jsonObject = [ordered]@{
    resolved_inputs    = $ResolvedInputs
    resolved_outputs   = $ResolvedOutputs
    constraints        = $Constraints
    decisions          = $Decisions
    assumptions        = $Assumptions
    codex_personality  = $CodexPersonality
    success_criteria   = $SuccessCriteria
}

$directory = Split-Path -Path $FilePath -Parent

if ($directory -and -not (Test-Path $directory)) {
    New-Item -Path $directory -ItemType Directory -Force | Out-Null
}

$jsonObject |
    ConvertTo-Json -Depth 5 |
    Set-Content -Path $FilePath -Encoding UTF8