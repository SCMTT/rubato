# Rubato - MIDI Tempo Adjuster

A simple and easy-to-use MIDI file tempo adjustment tool supporting speed-up, slow-down, and normal speed processing.

## Features

- 🎵 **Tempo Adjustment**: Supports speed multipliers from 0.1x to 3.0x
  - Less than 1.0x: Slow down
  - Greater than 1.0x: Speed up
  - Equal to 1.0x: Normal speed
- 📊 **File Information**: Display detailed MIDI file information
  - Duration
  - Number of instruments
  - Total number of notes
  - Number of tempo changes
  - Number of key signature changes
- 💾 **Export & Save**: Save processed MIDI files to a specified location
- 🖥️ **Graphical Interface**: Clean and intuitive GUI

## Requirements

- Python 3.7+
- Dependencies:
  - `pretty-midi` >= 0.2.10
  - `numpy` >= 1.21.0

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Program

```bash
python main.py
```

## Usage

1. **Select File**: Click the "选择文件" (Select File) button to choose the MIDI file you want to process
2. **View Information**: After loading, basic file information will be displayed
3. **Adjust Tempo**:
   - Use the slider or input field to set the speed multiplier (0.1 - 3.0)
4. **Process**: Click the "处理" (Process) button to apply the tempo adjustment
5. **Export**: Click the "导出" (Export) button to save the processed file

## Project Structure

```
rubato/
├── main.py           # Program entry point
├── gui.py            # Graphical user interface
├── controller.py     # Controller, coordinates modules
├── midi_processor.py # MIDI processing core module
└── requirements.txt  # Dependencies list
```

## Tech Stack

- **GUI Framework**: tkinter
- **MIDI Processing**: pretty-midi
- **Numerical Computing**: numpy

## License

This project is licensed under the MIT License.

## Contributing

Issues and Pull Requests are welcome!
