"""
Streamlit Web GUI for Dog MIDI System
Provides visual feedback and control interface
"""

import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import threading
import time
from dog_midi_system import DogMidiSystem
import pandas as pd
from collections import deque
import os

class DogMidiGUI:
    def __init__(self):
        self.system = None
        self.note_history = deque(maxlen=50)
        self.is_running = False
        
    def setup_page(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="🐕 Dog MIDI System",
            page_icon="🎹",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🐕 Dog MIDI Improvisation System")
        st.markdown("*A musical system where dogs can improvise on a MIDI keyboard and it sounds like a song!*")
    
    def sidebar_controls(self):
        """Create sidebar controls"""
        st.sidebar.header("🎛️ Controls")
        
        # MIDI file selection
        midi_files = [f for f in os.listdir('.') if f.endswith('.mid') or f.endswith('.midi')]
        if not midi_files:
            st.sidebar.warning("No MIDI files found in current directory")
            midi_file = st.sidebar.text_input("MIDI File Path", "totoro_theme.mid")
        else:
            midi_file = st.sidebar.selectbox("Select MIDI File", midi_files)
        
        # System parameters
        st.sidebar.subheader("🎵 Parameters")
        tempo = st.sidebar.slider("Tempo (BPM)", 60, 200, 120)
        timing_tolerance = st.sidebar.slider("Timing Tolerance", 0.1, 2.0, 0.5, 0.1)
        pitch_range = st.sidebar.slider("Pitch Correction Range", 1, 24, 12)
        randomness = st.sidebar.slider("Randomness Factor", 0.0, 1.0, 0.1, 0.05)
        
        # Control buttons
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("🚀 Start System", type="primary"):
                if not self.is_running:
                    self.start_system(midi_file, tempo, timing_tolerance, pitch_range, randomness)
        
        with col2:
            if st.button("⏹️ Stop System", type="secondary"):
                if self.is_running:
                    self.stop_system()
        
        # System status
        st.sidebar.subheader("📊 Status")
        if self.is_running:
            st.sidebar.success("🟢 System Running")
        else:
            st.sidebar.error("🔴 System Stopped")
        
        return midi_file, tempo, timing_tolerance, pitch_range, randomness
    
    def start_system(self, midi_file, tempo, timing_tolerance, pitch_range, randomness):
        """Start the MIDI system"""
        try:
            self.system = DogMidiSystem(midi_file)
            self.system.tempo = tempo
            self.system.timing_tolerance = timing_tolerance
            self.system.pitch_correction_range = pitch_range
            self.system.randomness_factor = randomness
            
            # Start system in background thread
            def run_system():
                self.system.start()
            
            system_thread = threading.Thread(target=run_system)
            system_thread.daemon = True
            system_thread.start()
            
            self.is_running = True
            st.sidebar.success("System started successfully!")
            
        except Exception as e:
            st.sidebar.error(f"Error starting system: {e}")
    
    def stop_system(self):
        """Stop the MIDI system"""
        if self.system:
            self.system.stop()
            self.is_running = False
            st.sidebar.info("System stopped")
    
    def display_current_status(self):
        """Display current system status"""
        col1, col2, col3, col4 = st.columns(4)
        
        if self.system and self.is_running:
            current_bar, current_beat = self.system.get_current_position()
            
            with col1:
                st.metric("Current Bar", f"{current_bar}")
            
            with col2:
                st.metric("Current Beat", f"{current_beat:.1f}")
            
            with col3:
                st.metric("Tempo", f"{self.system.tempo} BPM")
            
            with col4:
                st.metric("Notes Played", len(self.note_history))
        else:
            with col1:
                st.metric("Current Bar", "—")
            with col2:
                st.metric("Current Beat", "—")
            with col3:
                st.metric("Tempo", "—")
            with col4:
                st.metric("Notes Played", "—")
    
    def display_note_visualization(self):
        """Display note visualization"""
        st.subheader("🎼 Note Activity")
        
        if len(self.note_history) > 0:
            # Create a simple note history chart
            notes_df = pd.DataFrame(list(self.note_history))
            
            fig = px.scatter(
                notes_df, 
                x='time', 
                y='note',
                color='velocity',
                size='velocity',
                title="Recent Note Activity",
                labels={'time': 'Time', 'note': 'MIDI Note', 'velocity': 'Velocity'}
            )
            
            fig.update_layout(
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🎹 Start playing to see note visualization!")
    
    def display_original_melody(self):
        """Display the original melody structure"""
        st.subheader("🎵 Original Melody Structure")
        
        if self.system and self.system.original_notes:
            # Create a piano roll visualization
            notes_data = []
            for note in self.system.original_notes[:100]:  # Limit to first 100 notes
                notes_data.append({
                    'start_time': note.start_time,
                    'note': note.note,
                    'duration': note.duration,
                    'velocity': note.velocity,
                    'bar': note.bar
                })
            
            if notes_data:
                df = pd.DataFrame(notes_data)
                
                fig = px.scatter(
                    df,
                    x='start_time',
                    y='note',
                    color='bar',
                    size='velocity',
                    title="Original Melody (Piano Roll View)",
                    labels={'start_time': 'Time (seconds)', 'note': 'MIDI Note', 'bar': 'Bar'}
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Load a MIDI file to see the original melody structure")
    
    def display_instructions(self):
        """Display usage instructions"""
        with st.expander("📖 How to Use", expanded=False):
            st.markdown("""
            ### Setup Instructions:
            1. **Connect a MIDI keyboard** to your computer
            2. **Place a MIDI file** (like `totoro_theme.mid`) in the project directory
            3. **Click "Start System"** in the sidebar
            4. **Let your dog play** the MIDI keyboard!
            
            ### How It Works:
            - The system listens to MIDI input from your keyboard
            - It automatically corrects notes to match the original melody
            - Timing is adjusted to align with the song's rhythm
            - A little randomness is added to keep it musical and natural
            
            ### Features:
            - **Real-time note correction**: Wrong notes become right notes!
            - **Timing quantization**: Off-beat playing gets aligned
            - **Visual feedback**: See what notes are being played
            - **Customizable parameters**: Adjust correction sensitivity
            
            ### Tips:
            - Start with low randomness for more accurate correction
            - Increase timing tolerance if the dog plays very freely
            - The system works best with simple, melodic MIDI files
            """)
    
    def add_note_to_history(self, note, velocity):
        """Add a note to the visualization history"""
        self.note_history.append({
            'time': time.time(),
            'note': note,
            'velocity': velocity
        })
    
    def run(self):
        """Run the Streamlit GUI"""
        self.setup_page()
        
        # Sidebar controls
        midi_file, tempo, timing_tolerance, pitch_range, randomness = self.sidebar_controls()
        
        # Main content
        self.display_current_status()
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["🎼 Live Activity", "🎵 Original Melody", "📖 Instructions"])
        
        with tab1:
            self.display_note_visualization()
        
        with tab2:
            self.display_original_melody()
        
        with tab3:
            self.display_instructions()
        
        # Auto-refresh every second
        time.sleep(1)
        st.rerun()

def main():
    """Main function to run the GUI"""
    gui = DogMidiGUI()
    gui.run()

if __name__ == "__main__":
    main()
