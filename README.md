# Productivity Assistant

A productivity app that tracks app usage and allows you to set limits

## Goals

- Display the time spent on each app
- Chossing apps to block
- Blocking apps on certain days
- Blocking apps after reaching daily limit
- Blocking permenantly
- Daily reports
- Ignore lists
- Reminding of the usage time
- Stopping the app

## Postponed

- session blocking
- visit blocking
- Welcome screen on first launch

## Dependencies

- PyQt5
- pyqtgraph
- psutil
- pytz
- pywin32
- tzlocal
- PyInstaller

Run the following command to compile:
python -m PyInstaller --noconsole -n "Productivity Assistant" --clean --add-data "assets;assets" --noconfirm background.py