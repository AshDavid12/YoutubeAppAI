
# YouTube App - Speaker Identification

This Streamlit-based application uses OpenAI's GPT-4o model to identify speakers in YouTube video transcripts. It extracts the transcript and video description, processes them through a chatbot pipeline, and outputs speaker-identified segments.

## Getting started
### Installation
```
install streamlit   
install lanchchain_openai
install langchain_core.prompts.chat
install langchain_core.pydantic_v1 
install langchain.prompts 
install youtube_transcript_api 
install pytube 
install json
```
### Import


```
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from json import loads

```


### Run
Type in terminal: `streamlit run youtube_app_code.py`. 
Should pop up a web window with the app. 
Paste a url in the box and click Run!.
 



