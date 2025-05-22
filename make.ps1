# create docx from file structure

$ROOT_PATH = Split-Path $PSScriptRoot
$SRC_PATH = [IO.Path]::Combine($ROOT_PATH, "target")
$TARGET_PATH = [IO.Path]::Combine($ROOT_PATH, "src")
$NAME = "RSR00114_Rev. 3 (Test Report, TCD, AC Power Testing)"
$SRC = Join-Path $SRC_PATH $NAME
$TARGET = Join-Path $TARGET_PATH $NAME

# remove files that will be created
if (Test-Path "$TARGET.docx") {
	Remove-Item "$TARGET.docx" -verbose
}
if (Test-Path "$TARGET.zip") {
	Remove-Item "$TARGET.zip" -verbose
}

# zip
Compress-Archive "$SRC\*" "$TARGET.zip"

# change name 
Rename-Item "$TARGET.zip" "$TARGET.docx"
