import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import requests
from dotenv import load_dotenv

load_dotenv()

rapidapi_key = os.getenv("RAPIDAPI_KEY")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read user-library-read"
))


def search_track(track_name, artist_name=None, limit=1):
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"
    
    results = sp.search(q=query, type="track", limit=limit)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        info = {
            "id": track['id'],
            "name": track['name'],
            "artists": ', '.join([a['name'] for a in track['artists']]),
            "album": track['album']['name'],
            "release_date": track['album']['release_date'],
            "popularity": track['popularity'],
            "external_url": track['external_urls']['spotify']
        }
        return info
    else:
        return None


def get_audio_features(track_name, artist_name):
    url = "https://track-analysis.p.rapidapi.com/pktx/analysis"
    params = {
        'song': track_name,
        'artist': artist_name
    }
    headers = {
        'x-rapidapi-key': rapidapi_key,
        'x-rapidapi-host': 'track-analysis.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


# Edit these
track_name = "Blinding Lights"
artist_name = "The Weeknd"

query = f"track:{track_name} artist:{artist_name}"

track_info = search_track(track_name, artist_name)
audio_features = get_audio_features(track_name, artist_name)

if track_info:
    print(f"{track_info['name']} - {track_info['artists']}")
    print(f"Album: {track_info['album']}")
    print(f"Release Date: {track_info['release_date']}")
    print(f"Popularity: {track_info['popularity']}")
    print(f"Spotify URL: {track_info['external_url']}")
    print("Audio Features from SoundNet:")
    for key, value in audio_features.items():
        print(f"  {key}: {value}")
else:
    print("Track not found.")