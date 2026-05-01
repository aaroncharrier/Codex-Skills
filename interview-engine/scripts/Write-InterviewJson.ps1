<#
.SYNOPSIS
Creates or overwrites a structured JSON file.

.EXAMPLE
.\Write-InterviewJson.ps1 `
  -FilePath ".\interview.json" `
  -Confidence 0.75 `
  -Assumptions @("Assumption 1", "Assumption 2") `
  -ResolvedInputs @("Input 1") `
  -ResolvedOutputs @("Output 1") `
  -Constraints @("Constraint 1") `
  -Decisions @("Decision 1") `
  -OutputAssumptions @("Output assumption 1") `
  -CodexPersonality @("Direct", "Structured") `
  -SuccessCriteria @("Valid JSON", "Can be read by Codex") `
  -QuestionsFile ".\questions.json"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,

    [Parameter(Mandatory = $true)]
    [double]$Confidence,

    [string[]]$Assumptions = @(),

    [string[]]$ResolvedInputs = @(),
    [string[]]$ResolvedOutputs = @(),
    [string[]]$Constraints = @(),
    [string[]]$Decisions = @(),
    [string[]]$OutputAssumptions = @(),
    [string[]]$CodexPersonality = @(),
    [string[]]$SuccessCriteria = @(),

    [Parameter(Mandatory = $true)]
    [string]$QuestionsFile
)

if (-not (Test-Path $QuestionsFile)) {
    throw "Questions file not found: $QuestionsFile"
}

$questions = Get-Content -Path $QuestionsFile -Raw |
    ConvertFrom-Json -NoEnumerate

foreach ($q in $questions) {
    if ($q.type -is [array]) {
        throw "Each question must have exactly one type value, not an array."
    }
}

$jsonObject = [ordered]@{
    confidence = $Confidence
    assumptions = $Assumptions
    output = [ordered]@{
        resolved_inputs = $ResolvedInputs
        resolved_outputs = $ResolvedOutputs
        constraints = $Constraints
        decisions = $Decisions
        assumptions = $OutputAssumptions
        codex_personality = $CodexPersonality
        success_criteria = $SuccessCriteria
    }
    questions = @($questions)
}

$directory = Split-Path -Path $FilePath -Parent

if ($directory -and -not (Test-Path $directory)) {
    New-Item -Path $directory -ItemType Directory -Force | Out-Null
}

$jsonObject |
    ConvertTo-Json -Depth 20 |
    Set-Content -Path $FilePath -Encoding UTF8

if ((Test-Path $FilePath) -and ((Get-Item $FilePath).Length -gt 0)) {
    Remove-Item -Path $QuestionsFile -Force
}