param(
    [string]$ProjectRoot = ".",
    [string]$Date = (Get-Date -Format "yyyy-MM-dd")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-FieldValue {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Item,
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $property = $Item.PSObject.Properties[$Name]
    if ($null -eq $property) {
        return ""
    }

    if ($null -eq $property.Value) {
        return ""
    }

    return [string]$property.Value
}

function Normalize-Type {
    param(
        [string]$Value
    )

    $text = ""
    if ($null -ne $Value) {
        $text = $Value.Trim()
    }

    switch -Regex ($text) {
        "^(?i)task$" { return "Task" }
        "^(?i)bug$" { return "Bug" }
        "^(?i)decision$" { return "Decision" }
        "^(?i)research$" { return "Research" }
        "^(?i)meeting$" { return "Meeting" }
        "^(?i)achievement$" { return "Achievement" }
        "^(?i)follow[- ]?up$" { return "Follow-up" }
        default { return "" }
    }
}

function Normalize-Status {
    param(
        [string]$Value
    )

    $text = ""
    if ($null -ne $Value) {
        $text = $Value.Trim()
    }

    switch -Regex ($text) {
        "^(?i)open$" { return "Open" }
        "^(?i)(done|complete|completed)$" { return "Done" }
        "^(?i)blocked$" { return "Blocked" }
        "^(?i)deferred$" { return "Deferred" }
        default { return "" }
    }
}

function Format-FieldLine {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Label,
        [string]$Value
    )

    if ([string]::IsNullOrEmpty($Value)) {
        return "- ${Label}:"
    }

    return "- ${Label}: $Value"
}

$jsonInput = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($jsonInput)) {
    throw "Expected a JSON object or array on stdin."
}

$parsed = $jsonInput | ConvertFrom-Json
if ($parsed -is [System.Array]) {
    $items = $parsed
}
else {
    $items = @($parsed)
}

if ($items.Count -eq 0) {
    throw "Expected at least one scratch-note item."
}

$resolvedRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$targetPath = Join-Path -Path $resolvedRoot -ChildPath "scratch-notes.md"

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("## $Date")
$lines.Add("")

for ($index = 0; $index -lt $items.Count; $index++) {
    $item = $items[$index]

    $lines.Add((Format-FieldLine -Label "Date" -Value $Date))
    $lines.Add((Format-FieldLine -Label "Project" -Value (Get-FieldValue -Item $item -Name 'project')))
    $lines.Add((Format-FieldLine -Label "Type" -Value (Normalize-Type -Value (Get-FieldValue -Item $item -Name 'type'))))
    $lines.Add((Format-FieldLine -Label "Summary" -Value (Get-FieldValue -Item $item -Name 'summary')))
    $lines.Add((Format-FieldLine -Label "Action Items" -Value (Get-FieldValue -Item $item -Name 'action_items')))
    $lines.Add((Format-FieldLine -Label "Impact" -Value (Get-FieldValue -Item $item -Name 'impact')))
    $lines.Add((Format-FieldLine -Label "Status" -Value (Normalize-Status -Value (Get-FieldValue -Item $item -Name 'status'))))
    $lines.Add((Format-FieldLine -Label "Note" -Value (Get-FieldValue -Item $item -Name 'note')))

    if ($index -lt ($items.Count - 1)) {
        $lines.Add("")
    }
}

$block = [string]::Join("`n", $lines) + "`n"
$prefix = ""

if ((Test-Path -LiteralPath $targetPath) -and ((Get-Item -LiteralPath $targetPath).Length -gt 0)) {
    $prefix = "`n`n"
}

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::AppendAllText($targetPath, $prefix + $block, $utf8NoBom)
