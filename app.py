import streamlit as st
from dotenv import load_dotenv
load_dotenv()##load all the environment variables
import re
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""
Prompt for Note-Making Bot using GEMINI AI TOOL
Objective:

The goal is to generate comprehensive notes using the Cornell Method infused with the principles of Anvinshiki. The notes should cover diverse topics relevant for knowledge acquisition, competitive exams preparation (specifically UPSC, JEE, and other technical examinations), and provide detailed explanations with relevant pictures and genuine sources for further reference.

Structure of the Notes:
1. Topic Identification:

    Identify diverse topics within the domains of UPSC, JEE, and technical examinations.
    Prioritize topics based on importance, relevance, and frequency in exams.

2. Generate Overview:

    Provide a concise overview of each chosen topic, outlining key concepts and their applications.
    Include the significance of the topic in competitive exams.

3. Detailed Explanation:

    Utilize the Cornell Method to provide detailed explanations, breaking down complex concepts into simpler components.
    Ensure clarity in understanding and emphasize foundational principles.

4. Visual Aids:

    Incorporate relevant pictures, diagrams, and charts to enhance visual understanding.
    Ensure visual aids align with the explanations and serve as effective learning tools.

5. Anvinshiki Integration:

    Infuse principles of Anvinshiki, emphasizing holistic understanding and interconnectedness of topics.
    Establish relationships between different concepts to facilitate a deeper understanding.

6. Sources and References:

    Include genuine and reliable sources for each topic.
    Verify and provide clickable links for further studies, ensuring accessibility and authenticity.

7. Interactivity:

    Foster interactivity by incorporating quizzes, questions, and prompts for self-assessment.
    Encourage active engagement for better retention.

Expalin each section in great detail and use simple terms and provide glossary fro difficult terms . Articulate matter in an user appeasing manner and in detail with simple understanding examples.  

"""

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

st.set_page_config(page_title="YoutubeVideoSummarizer", page_icon="📚", layout="wide")
## Getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)    
    return response.text

st.title("Youtube Transcript to Detailed Notes Convertor")
youtube_link=st.text_input("Enter Youtube Video Link :")

##Extracting required youtube link fromthe provided youtube link 
def extract_youtube_link(youtube_link):
    # Use regular expression to find the video ID
    match = re.search(r"youtube\.com\/watch\?v=([^\&]+)", youtube_link)    
    # Check if there is a match
    if match:
        youtube_link = match.group(1)
        return "https://www.youtube.com/watch?v="+youtube_link
    else:
        return None

if youtube_link:
    # Extract video ID
    youtube_link = extract_youtube_link(youtube_link)
    print(youtube_link)
    
    if youtube_link:
        video_id=youtube_link.split("=")[1]
        print(video_id)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)
    print(transcript_text)
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
