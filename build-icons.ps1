# Generates the PWA icon set (sky/sun/mountain/wave mark) at 512, 192, and 180px.
Add-Type -AssemblyName System.Drawing

function New-Icon([int]$size, [string]$path) {
  $bmp = New-Object System.Drawing.Bitmap($size, $size)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

  # sky-to-sand gradient background
  $rect = New-Object System.Drawing.Rectangle(0, 0, $size, $size)
  $bg = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
    $rect,
    [System.Drawing.Color]::FromArgb(255, 207, 238, 245),
    [System.Drawing.Color]::FromArgb(255, 243, 227, 189),
    [System.Drawing.Drawing2D.LinearGradientMode]::Vertical)
  $g.FillRectangle($bg, $rect)

  # sun
  $sun = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 245, 197, 66))
  $g.FillEllipse($sun, [float]($size * 0.55), [float]($size * 0.10), [float]($size * 0.26), [float]($size * 0.26))

  # mountains
  $green = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 78, 158, 78))
  $pts = @(
    (New-Object System.Drawing.PointF([float]($size * 0.00), [float]($size * 0.80))),
    (New-Object System.Drawing.PointF([float]($size * 0.30), [float]($size * 0.28))),
    (New-Object System.Drawing.PointF([float]($size * 0.50), [float]($size * 0.55))),
    (New-Object System.Drawing.PointF([float]($size * 0.72), [float]($size * 0.36))),
    (New-Object System.Drawing.PointF([float]($size * 1.00), [float]($size * 0.80)))
  )
  $g.FillPolygon($green, $pts)

  # ocean wave band
  $teal = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 33, 150, 184))
  $wave = @(
    (New-Object System.Drawing.PointF([float]($size * 0.00), [float]($size * 0.80))),
    (New-Object System.Drawing.PointF([float]($size * 0.25), [float]($size * 0.73))),
    (New-Object System.Drawing.PointF([float]($size * 0.50), [float]($size * 0.80))),
    (New-Object System.Drawing.PointF([float]($size * 0.75), [float]($size * 0.73))),
    (New-Object System.Drawing.PointF([float]($size * 1.00), [float]($size * 0.80))),
    (New-Object System.Drawing.PointF([float]($size * 1.00), [float]($size * 1.00))),
    (New-Object System.Drawing.PointF([float]($size * 0.00), [float]($size * 1.00)))
  )
  $g.FillClosedCurve($teal, $wave, [System.Drawing.Drawing2D.FillMode]::Winding, 0.4)

  $g.Dispose()
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
  Write-Output "wrote $path"
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Icon 512 (Join-Path $root "icon-512.png")
New-Icon 192 (Join-Path $root "icon-192.png")
New-Icon 180 (Join-Path $root "apple-touch-icon.png")
