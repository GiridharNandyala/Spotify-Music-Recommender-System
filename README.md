# 🎵 Music Recommender System

A Full-Stack Music Recommendation Application built using **Streamlit**, **Python**, and the **Spotify Web API**. This project combines Natural Language Processing (NLP) text vectorization with live cloud API integration to deliver dynamic music recommendations and artwork fetching.

## 🚀 Features
- **Smart Recommendations:** Uses Content-Based Filtering driven by text mining.
- **Interactive UI:** A clean, responsive dashboard designed using Streamlit with a 5-column grid layout.
- **Live Spotify Integration:** Dynamically fetches high-resolution album covers and direct song links via `spotipy`.
- **Performance Optimized:** Implements Streamlit memory caching (`@st.cache_data`) for lightning-fast loading speeds.

## 🛠️ Tech Stack & Architecture

- **Frontend:** Streamlit
- **Backend & Logic:** Python, Pandas, Scikit-learn
- **Machine Learning / NLP:** `TfidfVectorizer`, `Cosine Similarity`
- **External API:** Spotify Web API (Spotipy library)

## 📦 How to Run This Project Locally

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/Music-Recommender-System.git](https://github.com/YOUR_USERNAME/Music-Recommender-System.git)
cd Music-Recommender-System


2. Install Dependencies
Make sure you have Python installed, then install the required libraries:

pip install streamlit pandas spotipy scikit-learn

3. Execution
Run the application using the following command:

streamlit run app.py


🔍 Core Logic (How Backend Works)
Dataset Optimization: The text data from songs is extracted and processed.
Vectorization: TfidfVectorizer converts song lyrics and metadata into multi-dimensional numerical vectors, stripping away common English stop words.
Similarity Indexing: cosine_similarity calculates the angular distance between vectors to find the top 5 closest matching tracks.
Live API Handshake: The app queries Spotify's global database using the song title to securely retrieve the original album art and external links.
