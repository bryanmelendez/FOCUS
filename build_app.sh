#!/bin/bash

# Build script for creating FocusPomodoro.app

echo "Building FocusPomodoro.app..."

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the app using PyInstaller
echo "Running PyInstaller..."
pyinstaller --name=FocusPomodoro \
    --windowed \
    --onedir \
    --clean \
    --noconfirm \
    --paths=src \
    --add-data="models:models" \
    --hidden-import=mediapipe \
    --hidden-import=mediapipe.tasks \
    --hidden-import=mediapipe.tasks.python \
    --hidden-import=mediapipe.tasks.python.vision \
    --hidden-import=cv2 \
    --hidden-import=numpy \
    --hidden-import=PySide6 \
    --hidden-import=PySide6.QtCore \
    --hidden-import=PySide6.QtWidgets \
    --hidden-import=PySide6.QtGui \
    --hidden-import=gui.main_window \
    --hidden-import=gui.regular_mode_view \
    --hidden-import=gui.pomodoro_mode_view \
    --hidden-import=model.regular_mode_model \
    --hidden-import=model.pomodoro_mode_model \
    --hidden-import=controller.regular_mode_controller \
    --hidden-import=controller.pomodoro_mode_controller \
    --hidden-import=controller.facial_imaging_controller \
    --hidden-import=utils.notification \
    --collect-all=mediapipe \
    --collect-all=PySide6 \
    --collect-all=cv2 \
    --copy-metadata=mediapipe \
    --copy-metadata=opencv-contrib-python \
    --osx-bundle-identifier=com.focus.pomodoro \
    src/main.py

# Check if build was successful
if [ -d "dist/FocusPomodoro.app" ]; then
    echo "Build successful!"
    echo "App location: dist/FocusPomodoro.app"
    echo ""
    echo "Testing app from terminal (check for errors):"
    ./dist/FocusPomodoro.app/Contents/MacOS/FocusPomodoro
else
    echo "Build failed!"
    exit 1
fi