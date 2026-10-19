$src = $PSScriptRoot
$uf2 = Join-Path $src "adafruit-circuitpython-qtpy_m0-en_US-10.3.1.uf2"
function Find-Drive($label) {
    (Get-CimInstance Win32_LogicalDisk | Where-Object { $_.VolumeName -eq $label } | Select-Object -First 1).DeviceID
}
$deadline = (Get-Date).AddMinutes(10)
$cp = Find-Drive "CIRCUITPY"
if (-not $cp) {
    "Waiting for QTPY_BOOT or CIRCUITPY..."
    while (-not ($boot = Find-Drive "QTPY_BOOT") -and -not ($cp = Find-Drive "CIRCUITPY")) {
        if ((Get-Date) -gt $deadline) { "Timed out waiting for board"; exit 1 }
        Start-Sleep -Seconds 2
    }
    if ($boot) {
        "Found QTPY_BOOT at $boot, copying CircuitPython"
        Copy-Item $uf2 "$boot\" -ErrorAction SilentlyContinue
        $t = (Get-Date).AddMinutes(2)
        while (-not ($cp = Find-Drive "CIRCUITPY")) {
            if ((Get-Date) -gt $t) { "CIRCUITPY never appeared after copying UF2"; exit 1 }
            Start-Sleep -Seconds 2
        }
    }
}
Start-Sleep -Seconds 3
"Found CIRCUITPY at $cp, copying lib and code.py"
New-Item -ItemType Directory -Force "$cp\lib" | Out-Null
Copy-Item "$src\lib\*" "$cp\lib\" -Recurse -Force
Copy-Item "$src\code.py" "$cp\code.py" -Force
Get-ChildItem $cp -Recurse | Select-Object FullName, Length | Format-Table -AutoSize | Out-String
Get-Content "$cp\boot_out.txt" -ErrorAction SilentlyContinue
"DONE"
