import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json
from langchain_core.output_parsers import StrOutputParser
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import re
import youtube_dl
from json import loads

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Helper functions

# Given url from user extract ID
def get_youtube_video_id(url):
    """
    Extracts the YouTube video ID from a given YouTube URL.
    Returns None if the URL format is invalid or no ID is found.
    """

    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    
   
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)  
    else:
        return None  

# Given video ID extract description
def get_description(video: YouTube) -> str:
    i: int = video.watch_html.find('"shortDescription":"')
    desc: str = '"'
    i += 20  # excluding the `"shortDescription":"`
    while True:
        letter = video.watch_html[i]
        desc += letter  # letter can be added in any case
        i += 1
        if letter == '\\':
            desc += video.watch_html[i]
            i += 1
        elif letter == '"':
            break
    return loads(desc)

# Given json data generates htlm 
def generate_html_from_json(json_data):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JSON to HTML</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                padding: 20px;
            }
            h1 {
                font-size: 24px;
                color: #007bff;
            }
            ul {
                list-style-type: none;
                padding-left: 0;
            }
            li {
                margin-bottom: 20px;
            }
            .speaker {
                font-weight: bold;
                color: #28a745;
            }
            .text {
                margin-top: 5px;
                margin-left: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Transcript </h1>
        <ul id="jsonOutput">
    """

    for segment in json_data['segments']:
        html_content += f"""
        <li>
            <div class="speaker">{segment['speaker']}</div>
            <div class="text">{segment['text']}</div>
        </li>
        """

    html_content += """
        </ul>
    </body>
    </html>
    """

    return html_content


# Pydantic Classes
class Segment(BaseModel):
    speaker: str
    text: str

class Transcript(BaseModel):
    segments: list[Segment]


# To AI system prompt
SYSTEM_PROMPT_FILTERING = SystemMessagePromptTemplate.from_template(
    """
    you will be given the script and short description of a video. Please return the script with speaker identification. 
    For each speaker show everyhthing they said in one segment until another speaker spoke.
    Add punctuation to the script.
    """
)

# Human prompt
TRANSCRIPT_MESSAGE_FILTER = HumanMessagePromptTemplate.from_template(
    """
    script: {script}
    title: {title}
    description: {desc}
    """
)


prompt = ChatPromptTemplate.from_messages([
    SYSTEM_PROMPT_FILTERING,
    TRANSCRIPT_MESSAGE_FILTER
])




# Langchain LCEL 
model = ChatOpenAI(model="gpt-4o", temperature=0)
chain = prompt | model.with_structured_output(Transcript) 

# Streamlit input
urlinput = st.text_input("Insert Vidoe URL")




def buttonTrue(user_input):
    # Needed info from youtube api
    id = get_youtube_video_id(urlinput)
    script = YouTubeTranscriptApi.get_transcript(id)
    video = YouTube(urlinput)
    video_title = video.title
    video_description = get_description(video) 

    # invoking chain with script description and title - this connects to the human prompt 
    response = chain.invoke({"script": script, "desc": video_description, "title": video_title})
    response_dict = response.dict() #convert json to dictionary 
    html_content = generate_html_from_json(response_dict) #get html template from dictionary


    #streamlit display
    st.title("Youtube App - Speaker Idintification")
    st.write(f" Title of Video: {video_title}")
    st.html(html_content) #send html to streamlit to display


if st.button('Run!'):
    if urlinput: 
        buttonTrue(urlinput)
