import tkinter as tk
from tkinter import messagebox
import requests
import re

# Function to extract video ID from URL
def extract_video_id(url):
    video_id = None
    # Handle different possible YouTube URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)',  # youtu.be/<video_id>
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/.*v=([a-zA-Z0-9_-]+)',  # youtube.com/watch?v=<video_id>
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)',  # youtube.com/embed/<video_id>
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]+)',  # youtube.com/v/<video_id>
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/.*\/([a-zA-Z0-9_-]+)'  # youtube.com/anything/<video_id>
    ]

    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            video_id = match.group(1)
            break

    return video_id

# Function to fetch transcript
def get_transcript():
    video_url = url_entry.get()
    if not video_url:
        messagebox.showerror("Input Error", "Please enter a YouTube video URL.")
        return

    video_id = extract_video_id(video_url)
    if not video_id:
        messagebox.showerror("URL Error", "Invalid YouTube URL.")
        return

    try:
        # Replace 'API_URL' with the actual API endpoint you found on GitHub
        response = requests.get(f"API_URL?video_id={video_id}")
        response.raise_for_status()
        transcript = response.json().get('transcript', 'No transcript available.')

        # Display the transcript in the text widget
        transcript_text.delete("1.0", tk.END)
        transcript_text.insert(tk.END, transcript)

    except requests.RequestException as e:
        messagebox.showerror("API Error", f"An error occurred while fetching the transcript: {e}")

# Create main application window
root = tk.Tk()
root.title("YouTube Transcript Fetcher")

# Create and place widgets
tk.Label(root, text="YouTube Video URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

get_transcript_button = tk.Button(root, text="Get Transcript", command=get_transcript)
get_transcript_button.pack(pady=10)

transcript_text = tk.Text(root, height=20, width=80)
transcript_text.pack(pady=10)

# Run the application
root.mainloop()
