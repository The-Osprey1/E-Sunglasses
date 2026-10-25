# Copies bench test 2's code.py and valve_drive.py onto the CIRCUITPY drive.
# CircuitPython is already on the board from bench test 1.
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
Copy-Item "$src\valve_drive.py" "$cp\valve_drive.py" -Force
Copy-Item "$src\code.py" "$cp\code.py" -Force
"Copied code.py and valve_drive.py. The board restarts by itself."
"DONE"
