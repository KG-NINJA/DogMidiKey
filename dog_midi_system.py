"""
Dog MIDI Improvisation System
A musical system where dogs can improvise on a MIDI keyboard and it sounds like a song.
"""

import mido
import pretty_midi
import pygame.midi
import numpy as np
import threading
import time
import random
from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Tuple
import json

@dataclass
class NoteEvent:
    """Represents a MIDI note event with timing information"""
    note: int
    velocity: int
    start_time: float
    duration: float
    bar: int
    beat: float

class DogMidiSystem:
    def __init__(self, midi_file_path: str):
        """Initialize the Dog MIDI System"""
        self.midi_file_path = midi_file_path
        self.original_notes = []
        self.current_bar = 0
        self.current_beat = 0.0
        self.tempo = 120  # BPM
        self.time_signature = (4, 4)  # 4/4 time
        self.is_playing = False
        self.start_time = None
        
        # MIDI setup
        pygame.midi.init()
        self.midi_input = None
        self.midi_output = None
        
        # Correction parameters
        self.timing_tolerance = 0.5  # seconds
        self.pitch_correction_range = 12  # semitones
        self.randomness_factor = 0.1  # 0-1, amount of randomness to add
        
        # Load and analyze the original MIDI file
        self.load_midi_file()
        self.setup_midi_devices()
        
    def load_midi_file(self):
        """Load and analyze the original MIDI file"""
        try:
            midi_data = pretty_midi.PrettyMIDI(self.midi_file_path)
            
            # Extract tempo and time signature
            if midi_data.get_tempo_changes()[1]:
                self.tempo = midi_data.get_tempo_changes()[1][0]
            
            # Extract notes from all instruments
            for instrument in midi_data.instruments:
                if not instrument.is_drum:
                    for note in instrument.notes:
                        # Calculate bar and beat position
                        beat_duration = 60.0 / self.tempo
                        beats_per_bar = self.time_signature[0]
                        
                        total_beats = note.start / beat_duration
                        bar = int(total_beats // beats_per_bar)
                        beat = total_beats % beats_per_bar
                        
                        note_event = NoteEvent(
                            note=note.pitch,
                            velocity=note.velocity,
                            start_time=note.start,
                            duration=note.end - note.start,
                            bar=bar,
                            beat=beat
                        )
                        self.original_notes.append(note_event)
            
            # Sort notes by start time
            self.original_notes.sort(key=lambda x: x.start_time)
            print(f"Loaded {len(self.original_notes)} notes from MIDI file")
            print(f"Tempo: {self.tempo} BPM")
            
        except Exception as e:
            print(f"Error loading MIDI file: {e}")
            # Create a simple fallback melody (C major scale)
            self.create_fallback_melody()
    
    def create_fallback_melody(self):
        """Create a simple fallback melody if MIDI loading fails"""
        print("Creating fallback melody...")
        c_major_scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5
        beat_duration = 60.0 / self.tempo
        
        for i, note in enumerate(c_major_scale * 4):  # Repeat scale 4 times
            start_time = i * beat_duration
            bar = i // 8
            beat = (i % 8) / 2.0
            
            note_event = NoteEvent(
                note=note,
                velocity=80,
                start_time=start_time,
                duration=beat_duration * 0.8,
                bar=bar,
                beat=beat
            )
            self.original_notes.append(note_event)
    
    def setup_midi_devices(self):
        """Setup MIDI input and output devices"""
        try:
            # List available MIDI devices
            print("Available MIDI devices:")
            for i in range(pygame.midi.get_count()):
                info = pygame.midi.get_device_info(i)
                print(f"  {i}: {info[1].decode()} ({'Input' if info[2] else 'Output'})")
            
            # Find and setup input device
            input_id = None
            for i in range(pygame.midi.get_count()):
                info = pygame.midi.get_device_info(i)
                if info[2]:  # Is input device
                    input_id = i
                    break
            
            if input_id is not None:
                self.midi_input = pygame.midi.Input(input_id)
                print(f"Using MIDI input: {pygame.midi.get_device_info(input_id)[1].decode()}")
            else:
                print("No MIDI input device found")
            
            # Find and setup output device
            output_id = None
            for i in range(pygame.midi.get_count()):
                info = pygame.midi.get_device_info(i)
                if not info[2]:  # Is output device
                    output_id = i
                    break
            
            if output_id is not None:
                self.midi_output = pygame.midi.Output(output_id)
                print(f"Using MIDI output: {pygame.midi.get_device_info(output_id)[1].decode()}")
            else:
                print("No MIDI output device found")
                
        except Exception as e:
            print(f"Error setting up MIDI devices: {e}")
    
    def get_current_position(self) -> Tuple[int, float]:
        """Get current bar and beat position"""
        if not self.start_time:
            return 0, 0.0
        
        elapsed_time = time.time() - self.start_time
        beat_duration = 60.0 / self.tempo
        beats_per_bar = self.time_signature[0]
        
        total_beats = elapsed_time / beat_duration
        bar = int(total_beats // beats_per_bar)
        beat = total_beats % beats_per_bar
        
        return bar, beat
    
    def find_closest_note(self, input_note: int, current_bar: int, current_beat: float) -> Optional[NoteEvent]:
        """Find the closest matching note from the original melody"""
        # Get notes from current and nearby bars
        candidate_notes = []
        for note_event in self.original_notes:
            bar_diff = abs(note_event.bar - current_bar)
            if bar_diff <= 1:  # Look at current bar and adjacent bars
                candidate_notes.append(note_event)
        
        if not candidate_notes:
            return None
        
        # Find the best match based on pitch and timing
        best_note = None
        best_score = float('inf')
        
        for note_event in candidate_notes:
            # Calculate pitch difference
            pitch_diff = abs(note_event.note - input_note)
            if pitch_diff > self.pitch_correction_range:
                continue
            
            # Calculate timing difference
            beat_diff = abs(note_event.beat - current_beat)
            if beat_diff > self.timing_tolerance * self.tempo / 60:
                continue
            
            # Combined score (lower is better)
            score = pitch_diff * 0.7 + beat_diff * 0.3
            
            if score < best_score:
                best_score = score
                best_note = note_event
        
        return best_note
    
    def apply_randomness(self, note: int, velocity: int) -> Tuple[int, int]:
        """Apply controlled randomness to make it sound less robotic"""
        if random.random() < self.randomness_factor:
            # Small pitch variation
            note_variation = random.randint(-2, 2)
            note = max(0, min(127, note + note_variation))
            
            # Small velocity variation
            velocity_variation = random.randint(-10, 10)
            velocity = max(1, min(127, velocity + velocity_variation))
        
        return note, velocity
    
    def process_input_note(self, input_note: int, velocity: int):
        """
        Strict melody-following: Any input triggers the next note in the original melody sequence.
        """
        if not hasattr(self, 'melody_index'):
            self.melody_index = 0
        if not self.original_notes:
            print("No original melody loaded.")
            return

        # Get the next note in the melody
        note_event = self.original_notes[self.melody_index]
        self.melody_index = (self.melody_index + 1) % len(self.original_notes)

        corrected_note = note_event.note
        corrected_velocity = note_event.velocity

        # Optionally, add a little randomness to velocity
        corrected_note, corrected_velocity = self.apply_randomness(corrected_note, corrected_velocity)

        # Send only the strict melody note to output
        if self.midi_output:
            self.midi_output.note_on(corrected_note, corrected_velocity)
            threading.Timer(0.5, lambda: self.midi_output.note_off(corrected_note, 0)).start()

        print(f"Melody Step: {self.melody_index}/{len(self.original_notes)} -> Output: {corrected_note}")

    
    def listen_for_input(self):
        """Listen for MIDI input in a separate thread"""
        print("Listening for MIDI input... Press Ctrl+C to stop")
        
        while self.is_playing:
            if self.midi_input and self.midi_input.poll():
                midi_events = self.midi_input.read(10)
                
                for event in midi_events:
                    status = event[0][0]
                    note = event[0][1]
                    velocity = event[0][2]
                    
                    # Note on event
                    if 144 <= status <= 159 and velocity > 0:
                        self.process_input_note(note, velocity)
            
            time.sleep(0.01)  # Small delay to prevent CPU overload
    
    def start(self):
        """Start the dog MIDI system"""
        if not self.midi_input:
            print("No MIDI input device available. Cannot start system.")
            return
        
        self.is_playing = True
        self.start_time = time.time()
        
        print("🐕 Dog MIDI System started!")
        print("Let your dog play the keyboard - notes will be automatically corrected to sound musical!")
        
        # Start input listening in a separate thread
        input_thread = threading.Thread(target=self.listen_for_input)
        input_thread.daemon = True
        input_thread.start()
        
        try:
            while self.is_playing:
                current_bar, current_beat = self.get_current_position()
                print(f"\rBar: {current_bar}, Beat: {current_beat:.1f}", end="", flush=True)
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the dog MIDI system"""
        self.is_playing = False
        if self.midi_input:
            self.midi_input.close()
        if self.midi_output:
            self.midi_output.close()
        pygame.midi.quit()
        print("\n🐕 Dog MIDI System stopped!")

def main():
    """Main function to run the Dog MIDI System"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python dog_midi_system.py <midi_file_path>")
        print("Example: python dog_midi_system.py totoro_theme.mid")
        return
    
    midi_file_path = sys.argv[1]
    
    try:
        system = DogMidiSystem(midi_file_path)
        system.start()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
