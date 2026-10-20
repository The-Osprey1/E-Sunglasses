# Copies bench test 2's code.py onto the CIRCUITPY drive. CircuitPython and the sensor
# library are already on the board from bench test 1; if the library is missing, it is
# copied from ..\bench-test-1\lib when that folder exists.
$src = $PSScriptRoot
function Find-Drive($label) {
    (Get-CimInstance Win32_LogicalDisk | Where-Object { $_.VolumeName -eq $label } | Select-Object -First 1).DeviceID
}
$deadline = (Get-Date).AddMinutes(5)
"Waiting for the CIRCUITPY drive..."
while (-not ($cp = Find-Drive "CIRCUITPY")) {
    if ((Get-Date) -gt $deadline) { "Timed out. Is the QT Py plugged in? If it shows up as QTPY_BOOT, run bench test 1's installer first."; exit 1 }
    Start-Sleep -Seconds 2
}
"Found CIRCUITPY at $cp"
$lib1 = Join-Path (Split-Path $src -Parent) "bench-test-1\lib"
if (-not (Test-Path "$cp\lib\adafruit_veml7700.mpy") -and (Test-Path $lib1)) {
    "Copying the sensor library from bench-test-1"
    New-Item -ItemType Directory -Force "$cp\lib" | Out-Null
    Copy-Item "$lib1\*" "$cp\lib\" -Recurse -Force
}
Copy-Item "$src\code.py" "$cp\code.py" -Force
"Copied code.py. The board restarts by itself."
"DONE"
