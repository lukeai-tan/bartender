import os
import requests
from dotenv import load_dotenv

load_dotenv()

rapidapi_key = os.getenv("RAPIDAPI_KEY")

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

def print_audio_features(track_name, artist_name):
    audio_features = get_audio_features(track_name, artist_name)
    print("Audio Features from SoundNet:")
    for key, value in audio_features.items():
        print(f"  {key}: {value}")
