import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = st.secrets["YOUTUBE_API_KEY"]
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

st.set_page_config(page_title="Mini YouTube", layout="wide")

st.title("📺 Mini YouTube Clone")
st.write("Search and play YouTube videos using the YouTube Data API")

# Search bar
query = st.text_input("🔍 Enter search term", "")

# Search button
if st.button("Search") and query:
    params = {
        "part": "snippet",
        "q": query,
        "key": API_KEY,
        "maxResults": 9,
        "type": "video"
    }

    try:
        res = requests.get(SEARCH_URL, params=params)
        res.raise_for_status()
        results = res.json().get("items", [])
        
        if not results:
            st.warning("No videos found.")
        else:
            for i in range(0, len(results), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(results):
                        video = results[i + j]
                        video_id = video["id"]["videoId"]
                        title = video["snippet"]["title"]
                        channel = video["snippet"]["channelTitle"]
                        thumbnail = video["snippet"]["thumbnails"]["medium"]["url"]

                        with cols[j]:
                            st.image(thumbnail, width=320)
                            st.markdown(f"**{title}**")
                            st.caption(f"Channel: {channel}")
                            st.video(f"https://www.youtube.com/watch?v={video_id}")
    except requests.exceptions.RequestException as e:
        st.error("❌ Failed to connect to YouTube API")
        st.exception(e)
