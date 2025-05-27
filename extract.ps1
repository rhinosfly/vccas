# convert docx to normal directory which can be version controlled
# also create .md file which can be diffed

$ROOT_PATH = Split-Path $PSScriptRoot
$NAME = "test-report"
$SRC_PATH = [IO.Path]::Combine($ROOT_PATH, "src")
$SRC = Join-Path $SRC_PATH "$NAME"
$TARGET_PATH = [IO.Path]::Combine($ROOT_PATH, "target")
$TARGET = Join-Path $TARGET_PATH $NAME

# remove files that will be created
if (Test-Path "$TARGET.zip") {
	Remove-Item "$TARGET.zip" -Recurse -Verbose
}
if (Test-Path "$TARGET") {
	Remove-Item "$TARGET" -Recurse -Verbose
}

# copy under change name
# NOTE: copy necessary so I can keep the docx open in MS docs
Copy-Item "$SRC.docx" "$TARGET.zip"

# extract
Write-Output "`r`nEXTRACTING"
Expand-Archive "$TARGET.zip" $TARGET
Write-Output "DONE`r`n"

#convert
Write-Output "`r`nCONVERTING"
pandoc.exe "$SRC.docx" -o "$TARGET.pandoc.md"
pandoc.exe "$SRC.docx" -o "$TARGET.strict.md" -t markdown_strict
pandoc.exe "$SRC.docx" -o "$TARGET.org"
Write-Output "DONE`r`n"
