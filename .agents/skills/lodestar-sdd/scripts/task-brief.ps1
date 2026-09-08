[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$PlanFile,
    [Parameter(Mandatory = $true, Position = 1)][int]$TaskNumber,
    [Parameter(Mandatory = $true, Position = 2)][string]$OutFile
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $PlanFile -PathType Leaf)) {
    Write-Error "task-brief: no such plan file: $PlanFile"
    exit 1
}

$heading = "### Task $TaskNumber:"
$inside = $false
$lines = [System.Collections.Generic.List[string]]::new()

foreach ($line in Get-Content -LiteralPath $PlanFile) {
    if ($line.StartsWith($heading)) {
        $inside = $true
        $lines.Add($line)
        continue
    }
    if ($inside -and $line -match '^### Task ') {
        break
    }
    if ($inside) {
        $lines.Add($line)
    }
}

if ($lines.Count -eq 0) {
    Write-Error "task-brief: no '$heading' heading found in $PlanFile"
    exit 1
}

[System.IO.File]::WriteAllLines($OutFile, $lines)
Write-Output "wrote ${OutFile}: $($lines.Count) lines"
