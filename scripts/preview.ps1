# Build and serve RunicDocs locally with Quartz (needs Node 22+ and git).
# First run downloads Quartz into .quartz\ (ignored by git); later runs reuse it.
# Open http://localhost:8080 when the build finishes. Re-run after editing notes.
$ErrorActionPreference = "Stop"

$QuartzVersion = if ($env:QUARTZ_VERSION) { $env:QUARTZ_VERSION } else { "v5.0.0" }
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path ".quartz")) {
  git clone --depth 1 --branch $QuartzVersion https://github.com/jackyzha0/quartz.git .quartz
  Push-Location .quartz
  npm ci
  npx quartz plugin restore
  Pop-Location
}

if (Test-Path ".quartz\content") { Remove-Item -Recurse -Force ".quartz\content" }
Copy-Item -Recurse "content" ".quartz\content"
Copy-Item "quartz.config.yaml" ".quartz\quartz.config.yaml" -Force

Set-Location .quartz
npx quartz build --serve
