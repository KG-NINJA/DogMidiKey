# DogMidiKey
# 🐕 Dog MIDI Improvisation System

A musical system where dogs can improvise on a MIDI keyboard, and the output still sounds like a recognizable song!

## Features

- **Real-time MIDI input processing**: Listens to MIDI keyboard input
- **Intelligent note correction**: Snaps random notes to the closest matching notes from a reference melody
- **Timing quantization**: Aligns note timing to the song's rhythm
- **Controlled randomness**: Adds musical variation while maintaining song structure
- **Visual feedback**: Web GUI showing current position and note activity
- **Multiple interfaces**: Command-line and web-based GUI options

## How It Works

1. **Load Reference Song**: The system analyzes a MIDI file to understand the melody structure
2. **Listen for Input**: Captures real-time MIDI input from a connected keyboard
3. **Smart Correction**: 
   - Maps input notes to the closest matching notes in the reference melody
   - Adjusts timing to align with the song's rhythm
   - Applies controlled randomness to maintain musical feel
4. **Output**: Sends corrected notes to MIDI output device or software synthesizer

## Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Connect MIDI devices**:
   - Connect a MIDI keyboard for input
   - Ensure you have a MIDI output device or software synthesizer

3. **Prepare MIDI files**:
   - Place your reference MIDI files in the project directory
   - Or create a sample file using the included script

## Usage

### Command Line Interface

```bash
# Create a sample MIDI file first
python create_sample_midi.py

# Run the system with a MIDI file
python dog_midi_system.py totoro_theme.mid
```

### Web GUI Interface

```bash
# Launch the Streamlit web interface
streamlit run dog_midi_gui.py
```

Then open your browser to the displayed URL (usually `http://localhost:8501`)

## Configuration

### System Parameters

- **Timing Tolerance**: How strict the timing correction is (0.1-2.0 seconds)
- **Pitch Correction Range**: Maximum semitones to search for matching notes (1-24)
- **Randomness Factor**: Amount of musical variation to add (0.0-1.0)
- **Tempo**: Song tempo in BPM (60-200)

### MIDI Setup

The system automatically detects available MIDI devices. Make sure your:
- MIDI keyboard is connected and recognized by your system
- MIDI output device or software synthesizer is available
- Audio drivers are properly configured

## File Structure

```
FuwaCoKey/
├── dog_midi_system.py      # Core MIDI processing system
├── dog_midi_gui.py         # Streamlit web interface
├── create_sample_midi.py   # Sample MIDI file generator
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── totoro_theme.mid       # Sample MIDI file (created by script)
```

## Technical Details

### Note Correction Algorithm

1. **Temporal Analysis**: Determines current position in the song (bar/beat)
2. **Candidate Selection**: Finds notes from the reference melody near the current position
3. **Best Match**: Selects the closest note based on pitch and timing similarity
4. **Randomization**: Applies small variations to maintain musical interest

### Supported MIDI Features

- Note On/Off events
- Velocity sensitivity
- Real-time processing
- Multiple octave ranges
- Tempo following

## Troubleshooting

### Common Issues

**No MIDI devices found**:
- Check that your MIDI keyboard is connected
- Verify drivers are installed
- Try reconnecting the device

**No audio output**:
- Ensure MIDI output device is selected
- Check audio system configuration
- Verify software synthesizer is running

**Notes not correcting properly**:
- Adjust timing tolerance
- Check that MIDI file loaded correctly
- Verify the reference melody has notes in the expected range

### Debug Mode

Run with verbose output:
```bash
python dog_midi_system.py totoro_theme.mid --verbose
```

## Customization

### Adding New Songs

1. Place your MIDI file in the project directory
2. Use simple, melodic MIDI files for best results
3. Ensure the file has clear note timing and structure

### Adjusting Correction Behavior

Modify these parameters in the code:
- `timing_tolerance`: Stricter/looser timing correction
- `pitch_correction_range`: Wider/narrower pitch matching
- `randomness_factor`: More/less variation in output

## Future Enhancements

- [ ] Bark-triggered special effects
- [ ] Multiple instrument support
- [ ] Advanced harmony generation
- [ ] Machine learning-based correction
- [ ] Mobile app interface
- [ ] Recording and playback features

## License

This project is open source. Feel free to modify and distribute!

## Contributing

Contributions welcome! Areas for improvement:
- Better note correction algorithms
- Additional GUI features
- Support for more MIDI file formats
- Performance optimizations

---

*Let your dog become a musical genius! 🐕🎹🎵*
