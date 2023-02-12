import streamlit as st
from pytube import YouTube
from moviepy.editor import *
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import zipfile

st.title('Mashup Web Service')

singer_name = st.text_input('Enter singer name')
num_videos = st.number_input('Enter number of videos', min_value=1)
video_duration = st.number_input('Enter duration of each video (in seconds)', min_value=1)
email = st.text_input('Enter your email address')

if st.button('Create Mashup'):
    # Download N videos of X singer from Youtube
    search_query = YouTube("https://www.youtube.com/results?search_query=" + singer_name.replace(" ", "+"))
    videos = search_query.filter(type="video")[:num_videos]
    for video in videos:
        YouTube(video).streams.filter(only_audio=True).first().download()

    # Convert all the videos to audio
    for video_file in os.listdir():
        if video_file.endswith(".mp4"):
            video_path = os.path.abspath(video_file)
            audio_file = os.path.splitext(video_file)[0] + ".mp3"
            audio_path = os.path.abspath(audio_file)
            VideoFileClip(video_path).audio.write_audiofile(audio_path)
            os.remove(video_path)

    # Cut first Y sec audios from all downloaded files
    for audio_file in os.listdir():
        if audio_file.endswith(".mp3"):
            audio_path = os.path.abspath(audio_file)
            cut_file = os.path.splitext(audio_file)[0] + "_cut.mp3"
            cut_path = os.path.abspath(cut_file)
            AudioFileClip(audio_path).subclip(0, video_duration).write_audiofile(cut_path)
            os.remove(audio_path)

    # Merge all audios to make a single output file
    audio_files = [audio for audio in os.listdir() if audio.endswith("_cut.mp3")]
    audio_clips = [AudioFileClip(audio) for audio in audio_files]
    final_clip = concatenate_audioclips(audio_clips)
    final_clip.write_audiofile("output.mp3")

    # Zip the output file and send it via email
    zip_filename = "output.zip"
    with zipfile.ZipFile(zip_filename, 'w') as myzip:
        myzip.write("output.mp3")
    send_email(email, zip_filename)

    # Clean up all temporary files
    for file in os.listdir():
        if file.endswith(".mp3") or file.endswith("_cut.mp3") or file == "output.mp3" or file == zip_filename:
            os.remove(file)

    st.success('Mashup file sent to email')

def send_email(to, filename):
    from_email = "your_email@gmail.com"  # Change to your own Gmail address
    from_password = "your_password"  # Change to your own Gmail password
    subject = "Mashup file"
    message = "Please find attached the Mashup file"
    file = filename

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    with open(file, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header
