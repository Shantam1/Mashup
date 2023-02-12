import streamlit as st
import requests
import youtube_dl
import moviepy.editor as mp
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

# function to download the video from YouTube
def download_video(video_url):
    ydl_opts = {
        'outtmpl': 'temp.mp4'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# function to create the Mashup
def create_mashup(videos, duration):
    clips = []
    for video in videos:
        download_video(video)
        clip = mp.VideoFileClip("temp.mp4").subclip(0, duration)
        clips.append(clip)
    final_clip = mp.concatenate_videoclips(clips)
    final_clip.write_videofile("output.mp4")

# function to create and send zip file via email
def send_email(user, password, to, subject, body, files=[]):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = COMMASPACE.join(to)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    for file in files:
        with open(file, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(user, password)
    smtp.sendmail(user, to, msg.as_string())
    smtp.quit()

# Streamlit app code
st.title("Mashup Web Service")
singer_name = st.text_input("Enter the name of the singer:")
num_videos = st.number_input("Enter the number of videos:", min_value=1, max_value=10, step=1)
duration = st.number_input("Enter the duration of each video in seconds:", min_value=1, max_value=60, step=1)
email_id = st.text_input("Enter your email ID:")
submit = st.button("Create Mashup")

if submit:
    # get the video URLs from YouTube API
    response = requests.get("https://www.googleapis.com/youtube/v3/search", params={
        "part": "id",
        "type": "video",
        "q": singer_name,
        "maxResults": num_videos,
        "key": "YOUR_API_KEY"
    })
    video_ids = [item["id"]["videoId"] for item in response.json()["items"]]
    video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]

    # create the Mashup
    create_mashup(video_urls, duration)

    # create and send the zip file via email
    files = ["output.mp4"]
    zip_file = "mashup.zip"
    with zipfile.ZipFile(zip_file, "w") as zip:
        for file in files:
            zip.write(file)
    send_email("YOUR_EMAIL_ID", "YOUR_EMAIL_PASSWORD", [email_id], "Mashup Result")
