import streamlit as st
from dotenv import load_dotenv
load_dotenv()##load all the environment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a Youtube video summarizer. You will be yaking the transcript text and summarizing the entire video and providing the important summary in points within 200 or 250 words. Please provide summary of given text: """

##Getting the transcript from yt videos using the video_id from the url
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript= ""
        for i in transcript_text:
            transcript +=" "+ i["text"]

        return transcript

    except Exception as e:
        raise e


## Getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)    
    return response.text



st.title("Youtube Transcript to be Detailed Notes Convertor")
youtube_link=st.text_input("Enter Youtube Video Link :")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Your Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)