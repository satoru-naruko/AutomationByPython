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
- Screen comparison for verification (optional)
- Loop-only mode that repeats the steps without any screen comparison
- Configurable click sequences through JSON files
- Keyboard interrupt support (ESC to exit)

## Usage

The tool supports two main commands:

1. Execute automated clicking sequence:

```bash
python autoclick.py exec

# use a specific config file (default: data/config.json)
python autoclick.py exec data/config-loop-only.json
```

1. Show current mouse position (useful for configuration):

```bash
python autoclick.py show
```

## Configuration

Click sequences are configured using JSON files in the `data` directory. Example format:

```json
{
    "loop_count": 10,
    "comparison_region": {
        "start_x": 100,
        "start_y": 100,
        "end_x": 400,
        "end_y": 200
    },
    "standby_position": { "x": 100, "y": 100 },
    "comparison_threshold": 0.98,
    "retry_delay_seconds": 2,
    "post_sequence_delay_seconds": 2,
    "steps": [
        { "x": 100, "y": 100, "pre_click_delay": 3 },
        { "x": 200, "y": 150, "pre_click_delay": 2 }
    ]
}
```

### Loop only (no screen verification)

To simply repeat the steps `loop_count` times without screen comparison, omit
`comparison_region` / `standby_position`, or set `"screen_verification": false`
explicitly. See `data/config-loop-only.json`.

```json
{
    "screen_verification": false,
    "loop_count": 29,
    "post_sequence_delay_seconds": 2,
    "steps": [
        { "x": 100, "y": 100, "pre_click_delay": 5 }
    ]
}
```

- `screen_verification` (optional, boolean) - when omitted it defaults to
  `true` if `comparison_region` is present and `false` if it is not, so existing
  config files keep working unchanged.
- Setting `"screen_verification": true` without a `comparison_region` is a
  configuration error.
- Between loops the tool waits `post_sequence_delay_seconds`;
  `standby_position` / `retry_delay_seconds` / `comparison_threshold` are
  unused in this mode.

## Exit

Press `ESC` key to stop the automation at any time.
