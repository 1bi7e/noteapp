import tkinter as tk
from tkinter import messagebox
import re
import os
import openai
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Set your OpenAI API key here
client = OpenAI(
    api_key = "API_KEY",
)

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
        # Fetch the transcript using YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format the transcript as Text
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript)

        # Clean up the formatted text
        clean_text = re.sub(r'\s+', ' ', text_formatted).strip()
        
        # Display the cleaned transcript in the text widget
        transcript_text.delete("1.0", tk.END)
        transcript_text.insert(tk.END, clean_text)

        # Send the cleaned transcript to ChatGPT and get the response
        send_to_chatgpt(clean_text)

    except Exception as e:
        messagebox.showerror("API Error", f"An error occurred while fetching the transcript: {e}")

# Function to send the cleaned transcript to ChatGPT
def send_to_chatgpt(clean_text):
    prompt = (f"Create a detailed note from the transcript given below. Create also 10 review questions "
              f"that will help me understand the topic from the transcript.\n\n"
              f"transcript: {clean_text}")

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional tutor."},
                {"role": "user", "content": f"Create a detailed note from the transcript given below. Create also 10 review questions that will help me understand the topic from the transcript.\n\n{clean_text}"}
            ]
        )   
        answer = completion.choices[0].message.content
        print(answer)
        
        # Display the ChatGPT response in the text widget
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, answer)

    except Exception as e:
        messagebox.showerror("ChatGPT API Error", f"An error occurred while getting the response from ChatGPT: {e}")

# Create main application window
root = tk.Tk()
root.title("Notes from YT")

# Create and place widgets
tk.Label(root, text="Paste YouTube video URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

get_transcript_button = tk.Button(root, text="Get Transcript", command=get_transcript)
get_transcript_button.pack(pady=10)

transcript_text = tk.Text(root, height=10, width=80)
transcript_text.pack(pady=10)

response_text = tk.Text(root, height=10, width=80)
response_text.pack(pady=10)

# Run the application
root.mainloop()
