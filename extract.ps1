# convert docx to normal directory which can be version controlled
# also create .md file which can be diffed

$ROOT_PATH = Split-Path $PSScriptRoot
$NAME = "RSR00114_Rev. 3 (Test Report, TCD, AC Power Testing)"
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
if (Test-Path "$TARGET.md") {
	Remove-Item "$TARGET.md" -Recurse -Verbose
}


# copy under change name
# NOTE: copy necessary so I can keep the docx open in MS docs
Copy-Item "$SRC.docx" "$TARGET.zip"

# extract
Write-Output "`r`nExpand-Archive $TARGET.zip"
Expand-Archive "$TARGET.zip" $TARGET
Write-Output "DONE"

#convert
Write-Output "`r`npandoc.exe $SRC.docx -o $TARGET.md"
pandoc.exe "$SRC.docx" -o "$TARGET.md"
Write-Output "DONE`r`n"
