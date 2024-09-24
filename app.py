import moviepy.editor as mpy
import librosa
import numpy as np
import matplotlib.pyplot as plt
from moviepy.video.VideoClip import ImageClip

# Step 1: Load the MP3 and Extract Audio Data
audio_path = "my_music.mp3"  # Replace with your MP3 file path
y, sr = librosa.load(audio_path, sr=None)  # Load the MP3 file with original sample rate
duration = librosa.get_duration(y=y, sr=sr)  # Get the duration in seconds

# Step 2: Define the make_frame function to generate continuous waveform visualization
def make_frame(t):
    # Convert time to sample index
    n = int(t * sr)  # time `t` in seconds to sample index `n`
    
    # Get a 100ms slice of the waveform (for each frame)
    slice_duration = int(sr // 10)  
    audio_slice = y[n:n + slice_duration] if n + slice_duration < len(y) else y[n:]
    
    # Plot the waveform slice
    plt.figure(figsize=(8, 4))
    plt.plot(audio_slice, color='cyan')
    plt.ylim(-1, 1)  # Normalize the audio slice between -1 and 1
    plt.axis('off')  # Remove axes for a clean look
    
    # Save the plot as an image (which will be the frame for this time `t`)
    plt.savefig('frame.png', bbox_inches='tight', pad_inches=0)
    plt.close()  # Close the plot to avoid memory issues
    
    return mpy.ImageClip('frame.png').img  # Return the image of the waveform

# Step 3: Create Background Clip (Image/GIF/Video)
background_path = "cover1.jpg"  # Replace with your image or video path
background_clip = ImageClip(background_path, duration=duration)

# Step 4: Create the continuous waveform video clip
waveform_clip = mpy.VideoClip(make_frame, duration=duration)

# Step 5: Combine the background and the waveform clip
# Set positions to adjust where the waveform appears on the screen
final_clip = mpy.CompositeVideoClip([
    background_clip.set_position("center"),         # Background image
    waveform_clip.set_position(("center", "bottom"))  # Waveform at bottom
])

# Step 6: Add MP3 as the audio track
final_clip = final_clip.set_audio(mpy.AudioFileClip(audio_path))

# Step 7: Export the final video with audio and waveform
output_path = "music_visualizer_output.mp4"  # Output video file
final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
