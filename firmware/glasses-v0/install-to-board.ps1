# Copies the glasses program onto the CIRCUITPY drive. CircuitPython is already on the board.
# The parts go first and code.py goes last, so the board restarts into the finished program.
# A config.py already on the board is kept, so your tuning survives an update.
$src = $PSScriptRoot
$modules = "valve_drive.py", "light.py", "auto.py", "touch.py", "out.py", "controls.py", "console.py", "config.py"

function Find-Drive($label) {
    (Get-CimInstance Win32_LogicalDisk | Where-Object { $_.VolumeName -eq $label } | Select-Object -First 1)
}
function Round-Up($n) { [math]::Ceiling($n / 512.0) * 512 }

$deadline = (Get-Date).AddMinutes(5)
"Waiting for the CIRCUITPY drive..."
while (-not ($disk = Find-Drive "CIRCUITPY")) {
    if ((Get-Date) -gt $deadline) { "Timed out. Is the QT Py plugged in? If it shows up as QTPY_BOOT, run bench test 1's installer first."; exit 1 }
    Start-Sleep -Seconds 2
}
$cp = $disk.DeviceID
"Found CIRCUITPY at $cp"

# Keep the board's own config.py if there is one, so tuning isn't lost on an update.
$keepConfig = Test-Path "$cp\config.py"
if ($keepConfig) { "A config.py is already on the board. Keeping it (your settings). Delete it on the board first to get the standard one." }
$toCopy = @($modules | Where-Object { -not ($_ -eq "config.py" -and $keepConfig) }) + "code.py"

# Check there is room. The board's drive is small.
$need = 0
foreach ($f in $toCopy) {
    $newLen = (Get-Item "$src\$f").Length
    $new = Round-Up $newLen
    $old = 0
    if (Test-Path "$cp\$f") {
        $oldLen = (Get-Item "$cp\$f").Length
        $old = Round-Up $oldLen
    }
    $need += [math]::Max(0, $new - $old)
}
$free = (Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DeviceID -eq $cp }).FreeSpace
"Space needed about $([math]::Ceiling($need / 1024)) KB, free $([math]::Floor($free / 1024)) KB."
if ($free -lt $need + 2048) {
    if (Test-Path "$cp\lib") {
        "The board's drive is nearly full. The lib folder on it only holds the light sensor library"
        "that bench test 1 used. The glasses program doesn't need it (bench test 1's installer puts it back)."
        $answer = Read-Host "Type YES and press Enter to delete the lib folder from the board, or just press Enter to stop"
        if ($answer -ne "YES") { "Stopped. Nothing was changed."; exit 1 }
        Remove-Item "$cp\lib" -Recurse -Force
        "Removed lib."
    } else {
        "The board's drive is full and there is no lib folder to free space. Nothing was changed."
        exit 1
    }
}

foreach ($f in $toCopy) {
    Copy-Item "$src\$f" "$cp\$f" -Force
    "Copied $f"
}
"The board restarts by itself. Do not touch the touch-pad wires for the first few seconds."
"DONE"
