<#
.SYNOPSIS
Extracts question and your_answer from an interview JSON file.

.EXAMPLE
.\Extract-QuestionAnswers.ps1 `
  -FilePath ".\interview.json" `
  -OutputPath ".\question_answers.json"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,

    [Parameter(Mandatory = $false)]
    [string]$OutputPath
)

if (-not (Test-Path $FilePath)) {
    throw "Input JSON file not found: $FilePath"
}

$data = Get-Content -Path $FilePath -Raw | ConvertFrom-Json

if (-not $data.questions) {
    throw "No questions section found in: $FilePath"
}

$extracted = @(
    foreach ($q in $data.questions) {
        [ordered]@{
            question    = $q.question
            your_answer = $q.your_answer
        }
    }
)

$json = $extracted | ConvertTo-Json -Depth 5

if ($OutputPath) {
    $directory = Split-Path -Path $OutputPath -Parent

    if ($directory -and -not (Test-Path $directory)) {
        New-Item -Path $directory -ItemType Directory -Force | Out-Null
    }

    $json | Set-Content -Path $OutputPath -Encoding UTF8
}
else {
    $json
}