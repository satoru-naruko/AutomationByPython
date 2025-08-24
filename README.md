# Auto Click Automation Tool

This Python-based automation tool provides mouse control and screen comparison functionality for automated clicking and screen verification.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Features

- Mouse position tracking and automated clicking
- Screen comparison for verification
- Configurable click sequences through JSON files
- Keyboard interrupt support (ESC to exit)

## Usage

The tool supports two main commands:

1. Execute automated clicking sequence:

```bash
python autoclick.py exec
```

1. Show current mouse position (useful for configuration):

```bash
python autoclick.py show
```

## Configuration

Click sequences are configured using JSON files in the `data` directory. Example format:

```json
{
    "steps": [
        {
            "index": 1,
            "x": 100,
            "y": 100,
            "delay_seconds": 1
        },
        {
            "index": 2,
            "x": 100,
            "y": 100,
            "delay_seconds": 3
        }
    ]
}
```

## Exit

Press `ESC` key to stop the automation at any time.
