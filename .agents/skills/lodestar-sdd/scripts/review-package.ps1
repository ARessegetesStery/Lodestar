[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$OutFile,
    [Parameter(Mandatory = $true, Position = 1, ValueFromRemainingArguments = $true)][string[]]$Paths
)

$ErrorActionPreference = 'Stop'

if ($Paths.Count -eq 0) {
    Write-Error 'usage: review-package.ps1 OUTFILE PATH [PATH...]'
    exit 2
}

$root = (& git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($root)) {
    Write-Error 'review-package: current directory is not inside a Git repository'
    exit 1
}

$status = & git -C $root status --porcelain -- @Paths
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
if ([string]::IsNullOrWhiteSpace(($status -join "`n"))) {
    Write-Error "review-package: NO CHANGES under the given paths, in repo $root"
    Write-Error 'review-package: nothing to review -- check the paths and the working directory'
    exit 1
}

$package = [System.Collections.Generic.List[string]]::new()
$package.Add('# Review package (working tree; nothing is committed -- the owner commits after review)')
$package.Add('')
$package.Add('## Status of the paths under review')
$package.AddRange([string[]]$status)
$package.Add('')
$package.Add('## Diffstat (tracked files only)')
$package.AddRange([string[]](& git -C $root diff --stat -- @Paths))
$package.Add('')
$package.Add('## Diff of tracked, modified files (-U10)')
$package.AddRange([string[]](& git -C $root diff -U10 -- @Paths))
$package.Add('')
$package.Add('## Full contents of NEW (untracked) files')

$untracked = & git -C $root ls-files --others --exclude-standard -- @Paths
foreach ($path in $untracked) {
    if ([string]::IsNullOrWhiteSpace($path)) { continue }
    $package.Add('')
    $package.Add("### NEW FILE: $path")
    $package.Add('```')
    $package.AddRange([string[]](Get-Content -LiteralPath (Join-Path $root $path)))
    $package.Add('```')
}

[System.IO.File]::WriteAllLines($OutFile, $package)
$bytes = (Get-Item -LiteralPath $OutFile).Length
Write-Output "wrote ${OutFile}: $bytes bytes"
