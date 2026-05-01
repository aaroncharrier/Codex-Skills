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

function Convert-QuestionRecord {
  param($Question)

  [ordered]@{
    question_id = Trim-Scalar ([string]$Question.question_id)
    question = Trim-Scalar ([string]$Question.question)
    your_answer = Trim-Scalar ([string]$Question.your_answer)
  }
}

function Read-StateFromJson {
  param([string]$StatePath)

  $raw = Get-Content -Raw -LiteralPath $StatePath | ConvertFrom-Json
  $questions = @()
  foreach ($item in (Ensure-Array $raw.questions)) {
    if ($null -ne $item) {
      $questions += Convert-QuestionRecord $item
    }
  }

  [ordered]@{
    confidence = Trim-Scalar ([string]$raw.confidence)
    assumptionLines = @((Ensure-Array $raw.assumption_lines) | ForEach-Object { [string]$_ })
    outputLines = @((Ensure-Array $raw.output_lines) | ForEach-Object { [string]$_ })
    questions = $questions
    sourcePath = $StatePath
  }
}

function Read-StateFromYaml {
  param([string]$InputPath)

  $lines = Get-Content -LiteralPath $InputPath
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

  [ordered]@{
    confidence = $confidence
    assumptionLines = $assumptionLines
    outputLines = $outputLines
    questions = $questions
    sourcePath = $InputPath
  }
}

$sessionDir = (Resolve-Path -LiteralPath $SessionPath).Path
$statePath = Join-Path $sessionDir 'session_state.json'
$yamlPath = Join-Path $sessionDir 'interview_questions.yaml'

if (Test-Path -LiteralPath $statePath) {
  $state = Read-StateFromJson -StatePath $statePath
}
else {
  if (-not (Test-Path -LiteralPath $yamlPath)) {
    throw "Missing session_state.json and interview_questions.yaml in $sessionDir"
  }

  $state = Read-StateFromYaml -InputPath $yamlPath
}

$answered = @($state.questions | Where-Object { -not [string]::IsNullOrWhiteSpace($_.your_answer) })
$unanswered = @($state.questions | Where-Object { [string]::IsNullOrWhiteSpace($_.your_answer) })

$sessionName = Split-Path -Leaf $sessionDir
$outputDir = Join-Path $sessionDir 'session_prompts'
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$main = @()
$main += '# Session Prompt'
$main += ''
$main += "Session: $sessionName"
if ($state.confidence -ne '') {
  $main += "Confidence: $($state.confidence)"
}
$main += "Source: $($state.sourcePath)"
$main += ''

if ($state.assumptionLines.Count -gt 0) {
  $main += '## Assumptions'
  $main += '```yaml'
  $main += $state.assumptionLines
  $main += '```'
  $main += ''
}

if ($state.outputLines.Count -gt 0) {
  $main += '## Resolved Context'
  $main += '```yaml'
  $main += $state.outputLines
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
