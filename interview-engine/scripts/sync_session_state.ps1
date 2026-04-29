param(
  [Parameter(Mandatory = $true)]
  [string]$SessionPath
)

function Trim-Scalar {
  param([string]$Value)

  if ($null -eq $Value) {
    return ""
  }

  $text = $Value.Trim()
  if ($text.Length -ge 2) {
    if (($text.StartsWith('"') -and $text.EndsWith('"')) -or ($text.StartsWith("'") -and $text.EndsWith("'"))) {
      return $text.Substring(1, $text.Length - 2)
    }
  }

  return $text
}

$sessionDir = (Resolve-Path -LiteralPath $SessionPath).Path
$inputPath = Join-Path $sessionDir 'interview_questions.yaml'
if (-not (Test-Path -LiteralPath $inputPath)) {
  throw "Missing interview_questions.yaml at $inputPath"
}

$lines = Get-Content -LiteralPath $inputPath
$confidence = ""
$assumptionLines = @()
$outputLines = @()
$questions = @()

$section = ""
$readingQuestions = $false
$currentQuestion = $null

foreach ($line in $lines) {
  if ($line -match '^confidence:\s*(.*)$') {
    $confidence = Trim-Scalar $matches[1]
    continue
  }

  if ($line -match '^assumptions:\s*$') {
    $section = 'assumptions'
    continue
  }

  if ($line -match '^output:\s*$') {
    $section = 'output'
    continue
  }

  if ($line -match '^questions:\s*$') {
    $section = 'questions'
    continue
  }

  if ($line -match '^# === ACTIVE_ANSWER_BLOCK_START ===') {
    if ($null -ne $currentQuestion) {
      $questions += $currentQuestion
      $currentQuestion = $null
    }
    $section = ''
    $readingQuestions = $true
    continue
  }

  if (-not $readingQuestions) {
    if ($section -eq 'assumptions') {
      $assumptionLines += [string]$line
      continue
    }

    if ($section -eq 'output') {
      $outputLines += [string]$line
      continue
    }

    continue
  }

  if ($line -match '^\s*-\s*question_id:\s*(.*)$') {
    if ($null -ne $currentQuestion) {
      $questions += $currentQuestion
    }

    $currentQuestion = [ordered]@{
      question_id = Trim-Scalar $matches[1]
      question = ''
      your_answer = ''
    }
    continue
  }

  if ($null -eq $currentQuestion) {
    continue
  }

  if ($line -match '^\s+question:\s*(.*)$') {
    $currentQuestion.question = Trim-Scalar $matches[1]
    continue
  }

  if ($line -match '^\s+your_answer:\s*(.*)$') {
    $currentQuestion.your_answer = Trim-Scalar $matches[1]
    continue
  }
}

if ($null -ne $currentQuestion) {
  $questions += $currentQuestion
}

$confidenceValue = 0.0
if ($confidence -ne '') {
  [void][double]::TryParse($confidence, [ref]$confidenceValue)
}

$state = [ordered]@{
  session_name = Split-Path -Leaf $sessionDir
  source = $inputPath
  confidence = $confidenceValue
  ready_for_handoff = ($confidenceValue -ge 0.95)
  assumption_lines = $assumptionLines
  output_lines = $outputLines
  questions = @($questions)
}

$statePath = Join-Path $sessionDir 'session_state.json'
[System.IO.File]::WriteAllText($statePath, ($state | ConvertTo-Json -Depth 6), (New-Object System.Text.UTF8Encoding($false)))

Write-Output "Wrote session_state.json to $statePath"
