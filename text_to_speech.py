from moviepy.editor import VideoFileClip
import os
import re
import yt_dlp

def download_youtube_video():
    try:
        # Accept YouTube video URL from the user
        video_url = input("Enter the YouTube video URL: ")

        # Initialize the yt-dlp downloader
        ydl = yt_dlp.YoutubeDL()

        # Download the video
        info_dict = ydl.extract_info(video_url, download=True)
        print("Video downloaded successfully!")
        
        # Get the filename of the downloaded video
        video_filename = ydl.prepare_filename(info_dict)
        
        # Initialize moviepy video file
        video_clip = VideoFileClip(video_filename)

        # Extract audio file
        audio_clip = video_clip.audio
        audio_path = "youtube_audio.wav"
        audio_clip.write_audiofile(audio_path)

        print("Audio extracted successfully!")
        
        # Close the video clip
        video_clip.close()

        return audio_path

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to download YouTube video and extract audio
audio_path = download_youtube_video()
