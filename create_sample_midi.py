"""
Create a sample MIDI file for testing the Dog MIDI System
This creates a simple Totoro-like theme for demonstration
"""

import pretty_midi
import numpy as np

def create_totoro_theme():
    """Create a simple melody inspired by Totoro theme"""
    
    # Create a PrettyMIDI object
    midi = pretty_midi.PrettyMIDI()
    
    # Create an instrument (piano)
    piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
    
    # Define the melody (simplified Totoro-like theme)
    # Notes in MIDI numbers (C4 = 60)
    melody = [
        # Phrase 1
        (67, 0.0, 0.5),   # G4
        (69, 0.5, 0.5),   # A4
        (71, 1.0, 0.5),   # B4
        (72, 1.5, 1.0),   # C5
        (69, 2.5, 0.5),   # A4
        (67, 3.0, 1.0),   # G4
        
        # Phrase 2
        (65, 4.0, 0.5),   # F4
        (67, 4.5, 0.5),   # G4
        (69, 5.0, 0.5),   # A4
        (67, 5.5, 1.0),   # G4
        (65, 6.5, 0.5),   # F4
        (64, 7.0, 1.0),   # E4
        
        # Phrase 3 (repeat with variation)
        (67, 8.0, 0.5),   # G4
        (69, 8.5, 0.5),   # A4
        (71, 9.0, 0.5),   # B4
        (72, 9.5, 1.0),   # C5
        (74, 10.5, 0.5),  # D5
        (72, 11.0, 1.0),  # C5
        
        # Phrase 4 (ending)
        (69, 12.0, 0.5),  # A4
        (67, 12.5, 0.5),  # G4
        (65, 13.0, 0.5),  # F4
        (64, 13.5, 0.5),  # E4
        (60, 14.0, 2.0),  # C4 (long ending note)
    ]
    
    # Add notes to the piano instrument
    for note_pitch, start_time, duration in melody:
        note = pretty_midi.Note(
            velocity=80,
            pitch=note_pitch,
            start=start_time,
            end=start_time + duration
        )
        piano.notes.append(note)
    
    # Add some harmony (simple bass line)
    bass_notes = [
        (48, 0.0, 4.0),   # C3
        (53, 4.0, 4.0),   # F3
        (48, 8.0, 4.0),   # C3
        (55, 12.0, 4.0),  # G3
    ]
    
    for note_pitch, start_time, duration in bass_notes:
        note = pretty_midi.Note(
            velocity=60,
            pitch=note_pitch,
            start=start_time,
            end=start_time + duration
        )
        piano.notes.append(note)
    
    # Add the instrument to the MIDI object
    midi.instruments.append(piano)
    
    # Set tempo (120 BPM)
    midi.tempo_changes.append(pretty_midi.TempoChange(tempo=120, time=0))
    
    return midi

def main():
    """Create and save the sample MIDI file"""
    print("Creating sample Totoro-like theme MIDI file...")
    
    midi = create_totoro_theme()
    
    # Save the MIDI file
    output_file = "totoro_theme.mid"
    midi.write(output_file)
    
    print(f"Sample MIDI file created: {output_file}")
    print(f"Duration: {midi.get_end_time():.1f} seconds")
    print(f"Number of notes: {len(midi.instruments[0].notes)}")

if __name__ == "__main__":
    main()
