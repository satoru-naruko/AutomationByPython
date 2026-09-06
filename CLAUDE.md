# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based mouse automation tool that executes configurable click sequences with screen verification. It uses image comparison to verify screen state before proceeding with automation steps.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run automated click sequence (default config: data/config.json)
python autoclick.py exec

# Run with a specific config file
python autoclick.py exec data/config-loop-only.json

# Show current mouse position (for configuration)
python autoclick.py show
```

## Architecture

### Entry Point
- `autoclick.py` - Main script handling CLI arguments (`exec` or `show` modes)

### Core Libraries (in `lib/`)
- **mouse_controller/** - Wrapper around pyautogui for mouse movement and clicking
- **screen_comparator/** - Captures screen regions and compares against expected state using OpenCV template matching (threshold-based similarity)
- **esc_down_listener/** - Keyboard listener using pynput for ESC key to abort automation
- **rect/** - Helper class for screen region coordinates (converts start/end points to x,y,width,height tuples)

### Configuration
- **config/config.py** - Loads and validates JSON configuration files
- **data/*.json** - Click sequence definitions

### Execution Flow
1. Load JSON config with click steps and comparison region
2. Register expected screen state via `ScreenComparator.register_expected()`
3. Execute click sequence (move mouse, click, wait)
4. After each loop, compare current screen to expected state
5. If screen doesn't match, click standby position and retry until match
   (steps 2/4/5 are skipped when screen verification is disabled - the sequence
   is just repeated `loop_count` times)
6. ESC key terminates at any time via background keyboard listener thread

## Configuration Format

JSON config files support:
- `loop_count` - Number of times to repeat the sequence
- `steps` - Array of click actions with `index`, `x`, `y`, `delay_seconds`
- `comparison_region` - Screen area to verify with `start_x`, `start_y`, `end_x`, `end_y`
- `screen_verification` - Optional boolean. Defaults to whether `comparison_region`
  exists. Set to `false` to loop the steps without any screen comparison
  (see `data/config-loop-only.json`); `true` without a `comparison_region` raises
  a configuration error.

## Dependencies

- pyautogui - Mouse/keyboard automation
- opencv-python - Image comparison
- mss - Multi-monitor screen capture
- pynput - Keyboard input listening
- numpy - Image array handling
