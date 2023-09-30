import speech_recognition as sr
import os
import moviepy.editor as mp

# Specify the folder containing video files
video_folder = "temp_videos/"

def transcribe_audio_file(audio_file_path):
    """Transcribes an audio file to text.

    Args:
        audio_file_path: The path to the audio file.

    Returns:
        A string containing the transcribed text.
    """

    # Create a speech recognition object.
    r = sr.Recognizer()

    # Open the audio file.
    with sr.AudioFile(audio_file_path) as source:
        # Listen for the data (load audio to memory).
        audio_data = r.record(source)

    # Recognize (convert from speech to text).
    text = r.recognize_google(audio_data)

    return text

def write_text_to_notepad(text, output_file_path):
    """Writes text to a notepad file.

    Args:
        text: The text to write.
        output_file_path: The path to the output file.
    """

    with open(output_file_path, "w") as f:
        f.write(text)

#if __name__ == "__main__":
def video_to_text():
    # List all video files in the specified folder
    video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        audio_file_path = os.path.splitext(video_path)[0] + ".wav"

        # Load the video
        clip = mp.VideoFileClip(video_path)

        # Extract audio from the video and save it as a WAV file
        audio_clip = clip.audio
        audio_clip.write_audiofile(audio_file_path, codec="pcm_s16le")

        # Transcribe the audio file to text
        text = transcribe_audio_file(audio_file_path)

        # Determine the output text file path
        output_file_path = os.path.splitext(video_path)[0] + ".txt"

        # Write the transcribed text to a text file
        write_text_to_notepad(text, output_file_path)

        print(f"Transcribed {video_file} to {os.path.basename(output_file_path)}")

    print("Transcription of all video files is complete.")
