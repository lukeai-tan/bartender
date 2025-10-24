from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

# Example track (try a very popular track)
track_id = "3AiD7F0YjA5H5c3e41yr7D"  # "Blinding Lights" global release ID

# Fetch audio features
features = sp.audio_features([track_id])[0]
print(features)
