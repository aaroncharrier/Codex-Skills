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
      $assumptionLines += $line
      continue
    }

    if ($section -eq 'output') {
      $outputLines += $line
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

$answered = @($questions | Where-Object { -not [string]::IsNullOrWhiteSpace($_.your_answer) })
$unanswered = @($questions | Where-Object { [string]::IsNullOrWhiteSpace($_.your_answer) })

$sessionName = Split-Path -Leaf $sessionDir
$outputDir = Join-Path $sessionDir 'session_prompts'
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$main = @()
$main += '# Session Prompt'
$main += ''
$main += "Session: $sessionName"
if ($confidence -ne '') {
  $main += "Confidence: $confidence"
}
$main += "Source: $inputPath"
$main += ''

if ($assumptionLines.Count -gt 0) {
  $main += '## Assumptions'
  $main += '```yaml'
  $main += $assumptionLines
  $main += '```'
  $main += ''
}

if ($outputLines.Count -gt 0) {
  $main += '## Resolved Context'
  $main += '```yaml'
  $main += $outputLines
  $main += '```'
  $main += ''
}

$main += '## Answered Questions'
if ($answered.Count -eq 0) {
  $main += '- None yet.'
}
else {
  $main += '| ID | Question | Answer |'
  $main += '| --- | --- | --- |'

  foreach ($item in $answered) {
    $qid = $item.question_id -replace '\|', '\|'
    $questionText = $item.question -replace '\|', '\|'
    $answerText = $item.your_answer -replace '\|', '\|'
    $main += "| $qid | $questionText | $answerText |"
  }
}

$main += ''
$main += '## Prompt'
$main += 'Use the resolved context and the answered questions above as the source of truth.'
$main += 'Build the next artifact requested by this session without re-asking answered questions.'
if ($unanswered.Count -gt 0) {
  $main += 'If anything is still missing, use follow-up.md to collect only the unanswered items.'
}
$main += ''

$mainPath = Join-Path $outputDir 'prompt.md'
[System.IO.File]::WriteAllText($mainPath, ($main -join [Environment]::NewLine), (New-Object System.Text.UTF8Encoding($false)))

if ($unanswered.Count -gt 0) {
  $followUp = @()
  $followUp += '# Follow-up Questions'
  $followUp += ''
  $followUp += 'Ask only the unanswered questions below. Preserve the original wording unless a rewrite is needed for clarity.'
  $followUp += ''

  foreach ($item in $unanswered) {
    $followUp += "- $($item.question_id): $($item.question)"
  }

  $followUp += ''
  $followUp += '## Prompt'
  $followUp += 'Collect the missing answers and write them back into interview_questions.yaml.'
  $followUp += ''

  $followUpPath = Join-Path $outputDir 'follow-up.md'
  [System.IO.File]::WriteAllText($followUpPath, ($followUp -join [Environment]::NewLine), (New-Object System.Text.UTF8Encoding($false)))
}

Write-Output "Wrote session prompts to $outputDir"
