#!/usr/bin/env python3

import os
import subprocess
import shutil
import sys

# Configuration
APP_NAME = "KmlShpConvert"
MAIN_SCRIPT = "main.py"
APP_DIR = f"{APP_NAME}.AppDir"
OUTPUT_DIR = "output"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Clean previous build
if os.path.exists(APP_DIR):
    shutil.rmtree(APP_DIR)

# Create AppDir structure
os.makedirs(f"{APP_DIR}/usr/bin", exist_ok=True)

# Copy main script and resources
shutil.copy(MAIN_SCRIPT, f"{APP_DIR}/usr/bin/{APP_NAME}")

# Create a wrapper script
with open(f"{APP_DIR}/AppRun", "w") as f:
    f.write(f"#!/bin/bash\n\nHERE="$(dirname "$(readlink -f "${{0}}")")\ncd "${{HERE}}"\nexport PYTHONPATH="${{HERE}}/usr/lib/python3.8/site-packages"\nexec python3 usr/bin/{APP_NAME} "$@"\n")

# Make the wrapper executable
os.chmod(f"{APP_DIR}/AppRun", 0o755)

# Copy desktop file
desktop_content = f"""[Desktop Entry]
Name={APP_NAME}
Exec=AppRun
Icon={APP_NAME}
Type=Application
Categories=Utility;
Terminal=false
"""

with open(f"{APP_DIR}/{APP_NAME}.desktop", "w") as f:
    f.write(desktop_content)

# Copy icon
icon_path = "ui/resources/img/gdalicon.png"
if os.path.exists(icon_path):
    os.makedirs(f"{APP_DIR}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)
    shutil.copy(icon_path, f"{APP_DIR}/usr/share/icons/hicolor/256x256/apps/{APP_NAME}.png")

# Build AppImage using linuxdeploy
print("Building AppImage...")
subprocess.run([
    "linuxdeploy", 
    "--appdir", APP_DIR,
    "--output", "appimage"
], check=True)

# Move the AppImage to the output directory
appimage_file = f"{APP_NAME}-x86_64.AppImage"
if os.path.exists(appimage_file):
    shutil.move(appimage_file, f"{OUTPUT_DIR}/{appimage_file}")
    print(f"AppImage built successfully: {OUTPUT_DIR}/{appimage_file}")
else:
    print("Failed to build AppImage.")
    sys.exit(1)