import moviepy.editor as mpy
import librosa
import numpy as np
import matplotlib.pyplot as plt
from moviepy.video.VideoClip import ImageClip

# Load the MP3 and Extract Audio Data
audio_path = "my_music.mp3"  # Replace with your MP3 file path
y, sr = librosa.load(audio_path, sr=None)  # Load the MP3 file with original sample rate
duration = librosa.get_duration(y=y, sr=sr)  # Get the duration in seconds

# Function to generate a circular waveform
def make_circular_waveform(audio_slice):
    # Generate angles for the circular waveform
    angles = np.linspace(0, 2 * np.pi, len(audio_slice))
    
    # Create a circular wave using polar coordinates
    x = np.cos(angles) * (1 + audio_slice)  # Scale by audio amplitude
    y = np.sin(angles) * (1 + audio_slice)
    
    return x, y

# Define the make_frame function to generate continuous circular waveform visualization
def make_frame(t, audio_data, sample_rate):
    n = int(t * sample_rate)  # Convert time to sample index
    slice_duration = int(sample_rate // 10)  # This is the duration for each slice (100 ms)
    audio_slice = audio_data[n:n + slice_duration] if n + slice_duration < len(audio_data) else audio_data[n:]

    # Generate circular waveform coordinates
    x, y = make_circular_waveform(audio_slice)
    
    # Plot the circular waveform
    plt.figure(figsize=(8, 8), dpi=100)  # Make it square
    plt.plot(x, y, color='cyan', linewidth=3)  # Make lines bolder
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.axis('off')  # Remove axes for a clean look
    plt.gca().set_aspect('equal', adjustable='box')  # Equal aspect ratio
    
    # Save the plot as an image
    plt.savefig('frame.png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()  # Close the plot to avoid memory issues
    
    return mpy.ImageClip('frame.png').img  # Return the image of the waveform

# Create Background Clip (Image/GIF/Video)
background_path = "cover1.jpg"  # Replace with your image or video path
background_clip = ImageClip(background_path, duration=duration)

# Create the continuous circular waveform video clip
waveform_clip = mpy.VideoClip(lambda t: make_frame(t, y, sr), duration=duration)

# Combine the background and the waveform clip
final_clip = mpy.CompositeVideoClip([
    background_clip.set_position("center"),         # Background image
    waveform_clip.set_position(("center", "center"))  # Waveform at center
])

# Add MP3 as the audio track
final_clip = final_clip.set_audio(mpy.AudioFileClip(audio_path))

# Export the final video with audio and waveform
output_path = "music_visualizer_output.mp4"  # Output video file
final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
