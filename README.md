# CodeAlpha Task Automation

A Python-based JPG File Organizer developed as part of the CodeAlpha Python Programming Internship.

## Features

- Automatically moves JPG and JPEG files.
- Creates destination folders automatically.
- Prevents overwriting files with duplicate names.
- Supports recursive folder scanning.
- Dry-run mode to preview file movements.
- Logging system using Python logging.
- Error handling for file operations.
- Displays a summary of moved files and total size.
- Supports command-line arguments.

## Technologies Used

- Python
- os / pathlib
- shutil
- argparse
- logging

## How to Run

1. Install Python.
2. Clone this repository.
3. Open the project folder in VS Code.
4. Run:

```bash
python task_automation.py
```

You can also provide folders directly:

```bash
python task_automation.py --src "C:/Images" --dest "C:/Organized"
```

Preview without moving files:

```bash
python task_automation.py --src "C:/Images" --dest "C:/Organized" --dry-run
```

Include subfolders:

```bash
python task_automation.py --src "C:/Images" --dest "C:/Organized" --recursive
```

## Developer

Prageshwar Kumar

## Internship

CodeAlpha Python Programming Internship
