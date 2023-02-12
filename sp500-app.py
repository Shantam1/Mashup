import streamlit as st
import smtplib
import os
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pytube import YouTube
from youtube_search import YoutubeSearch
import pydub
from pydub import AudioSegment
import time
import requests
# from dotenv.main import load_dotenv
# load_dotenv()
st.set_page_config("Mashup🥁")
st.title("Mashup 🥁")

def download_audio_from_search(singer, n, m):
    results = YoutubeSearch(singer, max_results=m).to_dict()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    for i, result in enumerate(results):
        video_url = "https://www.youtube.com/watch?v=" + result["id"]
#         try:
        yt = YouTube(requests.get(video_url, headers=headers).text)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename=f"{singer}_{i}.mp4")

        audio = pydub.AudioSegment.from_file(f"{singer}_{i}.mp4")
        audio = audio[:n * 1000]
        audio.export(f"{singer}_{i}.mp3", format="mp3")
        
#         except:
        time.sleep(3)
#             continue
# def download_audio_from_search(singer, n, m):
#     results = YoutubeSearch(singer, max_results=m).to_dict()
#     for i, result in enumerate(results):
#         video_url = "https://www.youtube.com/watch?v=" + result["id"]
#         yt = YouTube(video_url)
#         stream = yt.streams.filter(only_audio=True).first()
#         stream.download(filename=f"{singer}_{i}.mp4")

#         audio = pydub.AudioSegment.from_file(f"{singer}_{i}.mp4")
#         audio = audio[:n * 1000]
#         audio.export(f"{singer}_{i}.mp3", format="mp3")
        # st.write(f"Audio of {n} seconds from {yt.title} downloaded and converted to MP3 successfully")

def combine_audio_files(singer, n, m):
    combined = AudioSegment.empty()
    for i in range(m):
        audio = AudioSegment.from_file(f"{singer}_{i}.mp3")
        combined += audio
    combined.export(f"combined.mp3", format="mp3")
    # st.write(f"All audio files combined into a single file: {singer}_combined.mp3")

def sendMail(recp):
    # Email details
    sender = st.secrets["SMTP_MAIL"]
    recipient = recp
    password = st.secrets["SMTP_PASS"]
    subject = 'Combined Audio File'
    # Create the message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    # Add the text
    text = MIMEText(f'Please find the attached the combined audio file of {singer}')
    msg.attach(text)
    # Add the audio file
    audi = MIMEAudio(open('combined.mp3', 'rb').read(), 'mp3')
    msg.attach(audi)
    # Send the email
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender, password)
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.quit()

singer = st.text_input("Singer Name:")
m = st.number_input("Nnumber of Videos:", min_value=10, max_value=50)
n = st.number_input("Duration of each Audio Clip (in seconds):", min_value=20, max_value=90)
recp = st.text_input("Email To:")
bt1 = st.button("Combine and Send Mail")


if bt1:
    # if download_audio_from_search(singer, n, m):
    # combine_audio_files(singer, n, m)
    # recp = st.text_input("Enter receiver email:")
    with st.spinner('Preparing Audio... (this may take upto a few minutes)'):
#         download_audio_from_search(singer, n, m)
#         combine_audio_files(singer, n, m)
#         sendMail(recp)
#         st.success('Your file was mailed successfully!')
        try:
            download_audio_from_search(singer, n, m)
            combine_audio_files(singer, n, m)
            sendMail(recp)
            st.success('Your file was mailed successfully!')
        except:
            st.error("Too much traffic at the moment, please try again in a few minutes")
    
        
    # if st.button("Send Mail"):       
    # st.success("Mail sent successfully!")
