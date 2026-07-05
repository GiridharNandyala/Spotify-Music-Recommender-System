import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Layout Setting
st.set_page_config(page_title="Music Recommender", layout="wide")

# --- Spotify API Configuration ---
CLIENT_ID = "db3fab49cbb648e0a875a399124b4d0a"
CLIENT_SECRET = "53ec4c0cc39a48c18200b04da1abb8ec"

try:
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except:
    sp = None

# --- Live Spotify Details Fetcher ---
def get_track_features(song_name, artist_name):
    query_encoded = urllib.parse.quote(f"{song_name} {artist_name}")
    fallback_link = f"https://open.spotify.com/search/{query_encoded}"
    
    if not sp:
        return "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500", fallback_link
    
    query = f"track:{song_name}"
    try:
        search_res = sp.search(q=query, type='track', limit=1)
        if search_res['tracks']['items']:
            track_data = search_res['tracks']['items'][0]
            cover_art = track_data['album']['images'][0]['url']
            spotify_link = track_data['external_urls']['spotify']
            return cover_art, spotify_link
    except:
        pass
    
    return "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500", fallback_link

# --- Data Loading ---
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv('spotify_millsongdata.csv')
       
        df = df.sample(5000, random_state=42).reset_index(drop=True)
        
        # TF-IDF & Similarity Matrix 
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['text'])
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        return df, similarity_matrix
    except FileNotFoundError:
        st.error("Error: 'spotify_millsongdata.csv' missing in your folder!")
        st.stop()


music, similarity = load_and_process_data()

# --- Recommendation Logic ---
def recommend(song):
    try:
        song_index = music[music['song'] == song].index[0]
        distances = similarity[song_index]
        songs_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_songs = []
        recommended_posters = []
        spotify_links = []
        
        for i in songs_list:
            track_name = music.iloc[i[0]].song
            artist_name = music.iloc[i[0]].artist
            recommended_songs.append(track_name)
            
            # Fetch image and link from Spotify API
            poster, link = get_track_features(track_name, artist_name)
            recommended_posters.append(poster)
            spotify_links.append(link)
            
        return recommended_songs, recommended_posters, spotify_links
    except:
        return [], [], []

# --- Main UI Layout ---
st.title('🎵 Music Recommender System')
st.write("---")

# Dropdown Box
selected_song = st.selectbox(
    'Type or Select a Song name:',
    music['song'].values
)

# Button Trigger
if st.button('Show Recommendation'):
    recommended_songs, recommended_posters, spotify_links = recommend(selected_song)
    
    if recommended_songs:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.image(recommended_posters[0], width=150)
            st.markdown(f"**{recommended_songs[0].title()}**")
            st.link_button("Listen", spotify_links[0])

        with col2:
            st.image(recommended_posters[1], width=150)
            st.markdown(f"**{recommended_songs[1].title()}**")
            st.link_button("Listen", spotify_links[1])

        with col3:
            st.image(recommended_posters[2], width=150)
            st.markdown(f"**{recommended_songs[2].title()}**")
            st.link_button("Listen", spotify_links[2])

        with col4:
            st.image(recommended_posters[3], width=150)
            st.markdown(f"**{recommended_songs[3].title()}**")
            st.link_button("Listen", spotify_links[3])

        with col5:
            st.image(recommended_posters[4], width=150)
            st.markdown(f"**{recommended_songs[4].title()}**")
            st.link_button("Listen", spotify_links[4])
    else:
        st.error("Error in generating recommendations.")