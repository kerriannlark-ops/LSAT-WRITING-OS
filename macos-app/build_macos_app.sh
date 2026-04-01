#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/build"
APP_NAME="Kerri LSAT Writing.app"
APP_DIR="$BUILD_DIR/$APP_NAME"
ZIP_PATH="$BUILD_DIR/Kerri LSAT Writing.zip"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"
WEB_DIR="$RESOURCES_DIR/Web"

rm -rf "$APP_DIR"
rm -f "$ZIP_PATH"
mkdir -p "$MACOS_DIR" "$WEB_DIR"

swiftc \
  -parse-as-library \
  "$ROOT_DIR/macos-app/LSATWritingMac.swift" \
  -framework Cocoa \
  -framework WebKit \
  -o "$MACOS_DIR/KerriLSATWriting"

cp "$ROOT_DIR/macos-app/Info.plist" "$CONTENTS_DIR/Info.plist"
cp "$ROOT_DIR/macos-app/AppIcon.icns" "$RESOURCES_DIR/AppIcon.icns"
cp "$ROOT_DIR/index.html" "$WEB_DIR/index.html"
cp "$ROOT_DIR/manifest.webmanifest" "$WEB_DIR/manifest.webmanifest"
cp "$ROOT_DIR/service-worker.js" "$WEB_DIR/service-worker.js"
cp "$ROOT_DIR/icon.svg" "$WEB_DIR/icon.svg"
mkdir -p "$WEB_DIR/output"
cp -R "$ROOT_DIR/output/." "$WEB_DIR/output/"

python3 - <<PY
import json
from pathlib import Path

manifest = {
    "metadata": {
        "generated_on": "2026-03-31",
        "description": "Private local reference document manifest for the macOS LSAT Writing app."
    },
    "documents": [
        {
            "id": "module-docx",
            "path": "/Users/kerriannlark/Desktop/law school admissions package 2026/LSAT_Learning_Module.docx"
        },
        {
            "id": "module-pptx",
            "path": "/Users/kerriannlark/Desktop/law school admissions package 2026/LSAT_Learning_Module.pptx"
        },
        {
            "id": "argumentative-notes",
            "path": "/Users/kerriannlark/Library/CloudStorage/OneDrive-KentStateUniversity/argumentative notes from sources.docx"
        },
        {
            "id": "study-guide-source",
            "path": "/Users/kerriannlark/Library/CloudStorage/OneDrive-KentStateUniversity/LSAT ARGUMENTATIVE WRITING STUDY GUIDE.docx"
        },
        {
            "id": "practice-essay-source",
            "path": "/Users/kerriannlark/Library/CloudStorage/OneDrive-KentStateUniversity/LSAT Practice Argumentative Essay.docx"
        },
        {
            "id": "writing-notes-source",
            "path": "/Users/kerriannlark/Library/CloudStorage/OneDrive-KentStateUniversity/LSAT ARGUMENTATIVE WRITING NOTES.docx"
        },
        {
            "id": "document2-source",
            "path": "/Users/kerriannlark/Library/CloudStorage/OneDrive-KentStateUniversity/Document2.docx"
        },
        {
            "id": "document6-source",
            "path": "/Users/kerriannlark/Library/CloudStorage/OneDrive-KentStateUniversity/Document (6).docx"
        }
    ]
}

Path("$WEB_DIR/output/local_reference_library.json").write_text(json.dumps(manifest, indent=2))
PY

ditto -c -k --sequesterRsrc --keepParent "$APP_DIR" "$ZIP_PATH"

echo "Built macOS app bundle at:"
echo "  $APP_DIR"
echo "Packaged zip at:"
echo "  $ZIP_PATH"
