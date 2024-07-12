
# YouTube App - Speaker Identification

This Streamlit-based application uses OpenAI's GPT-4o model to identify speakers in YouTube video transcripts. It extracts the transcript and video description, processes them using lanchain, and outputs speaker-identified segments.

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
#### Using poetry for dependencies:  
```
install poetry 
poetry shell 
```

#### Set up your API Key: 
1. Can use streamlit interface and in code use `st.secretes["name of your key variable"]`.
2. Insert key directly to code ` os.environ["OPENAI_API_KEY"] = "your_key_string" `
* make sure to use python 3.11 in order to run streamlit

### Run
Type in terminal: `streamlit run youtube_app_code.py`. 
Should pop up a web window with the app. 
Paste a url in the box and click Run!.  
 
Alternitivly, paste this link in a browser - https://youtubeappai-7dp5fkqccpx6eokchqcz5a.streamlit.app/ 

## User Interface
<img width="689" alt="Screenshot 2024-07-11 at 9 47 05 AM" src="https://github.com/AshDavid12/YoutubeAppAI/assets/140085047/83bb0eea-4e70-4a8c-9b1d-bba9c0fc3d19">
