# render_pages.ps1 - pdftoppm wrapper for the /YanaNotesGenerator pipeline.
#
# Full render (vision extraction input, 150 DPI keeps image tokens low):
#   .\render_pages.ps1 -Pdf "sources\Part1.pdf" -OutDir "pages-cache\Part1"
#
# Figure crop (high quality cut from the ORIGINAL page for the notes):
#   .\render_pages.ps1 -Pdf "sources\Part1.pdf" -Page 12 `
#       -X 210 -Y 340 -W 620 -H 410 -OutFile "figures\fig03_rtd_bridge.png"
#   Crop coordinates are pixels measured on the 150 DPI render (-CoordsDpi);
#   they are scaled automatically to the output DPI (300 for crops).

param(
    [Parameter(Mandatory = $true)][string]$Pdf,
    [string]$OutDir,                 # full-render mode: output folder for page PNGs
    [int]$Dpi = 0,                   # default: 150 full render, 300 crop
    [int]$Page = 0,                  # crop mode: single page number (1-based)
    [int]$X = -1, [int]$Y = -1, [int]$W = 0, [int]$H = 0,
    [int]$CoordsDpi = 150,           # DPI at which X/Y/W/H were measured
    [string]$OutFile                 # crop mode: output PNG path
)

if (-not (Test-Path $Pdf)) { Write-Error "PDF not found: $Pdf"; exit 1 }

$isCrop = ($Page -gt 0 -and $W -gt 0 -and $H -gt 0)

if ($isCrop) {
    if (-not $OutFile) { Write-Error "Crop mode needs -OutFile"; exit 1 }
    if ($Dpi -eq 0) { $Dpi = 300 }
    $scale = $Dpi / $CoordsDpi
    $sx = [int][math]::Round($X * $scale)
    $sy = [int][math]::Round($Y * $scale)
    $sw = [int][math]::Round($W * $scale)
    $sh = [int][math]::Round($H * $scale)
    $outBase = $OutFile -replace '\.png$', ''
    $outParent = Split-Path $OutFile -Parent
    if ($outParent -and -not (Test-Path $outParent)) { New-Item -ItemType Directory -Force $outParent | Out-Null }
    & pdftoppm -png -r $Dpi -f $Page -l $Page -x $sx -y $sy -W $sw -H $sh -singlefile $Pdf $outBase
    if ($LASTEXITCODE -ne 0) { Write-Error "pdftoppm crop failed"; exit 1 }
    Write-Output "Cropped page $Page of '$Pdf' -> $OutFile ($Dpi DPI, box ${sx},${sy} ${sw}x${sh})"
}
else {
    if (-not $OutDir) { Write-Error "Full-render mode needs -OutDir"; exit 1 }
    if ($Dpi -eq 0) { $Dpi = 150 }
    if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force $OutDir | Out-Null }
    & pdftoppm -png -r $Dpi $Pdf (Join-Path $OutDir "page")
    if ($LASTEXITCODE -ne 0) { Write-Error "pdftoppm render failed"; exit 1 }
    $count = (Get-ChildItem $OutDir -Filter "page-*.png").Count
    Write-Output "Rendered $count pages of '$Pdf' -> $OutDir ($Dpi DPI)"
}
