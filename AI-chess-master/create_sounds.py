import numpy as np
from scipy.io import wavfile

def create_move_sound():
    # Parameters for move sound
    duration = 0.15  # seconds
    fs = 44100  # sampling frequency
    t = np.linspace(0, duration, int(fs * duration))
    
    # Create a simple "click" sound
    frequency = 1000
    signal = np.sin(2 * np.pi * frequency * t) * np.exp(-5 * t)
    
    # Normalize and convert to 16-bit integer
    signal = np.int16(signal * 32767)
    
    # Save the file
    wavfile.write('sounds/move.wav', fs, signal)

def create_capture_sound():
    # Parameters for capture sound
    duration = 0.2  # seconds
    fs = 44100  # sampling frequency
    t = np.linspace(0, duration, int(fs * duration))
    
    # Create a more complex sound for capture
    f1, f2 = 800, 1200
    signal = (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)) * np.exp(-4 * t)
    
    # Normalize and convert to 16-bit integer
    signal = np.int16(signal * 32767)
    
    # Save the file
    wavfile.write('sounds/capture.wav', fs, signal)

if __name__ == "__main__":
    create_move_sound()
    create_capture_sound()
    print("Sound files created successfully in the 'sounds' directory.") 