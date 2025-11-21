import requests
from spotipy_utils import *

BASE_URL = "https://api.reccobeats.com/v1"


def get_reccobeats_track_id(spotify_id):
    """
    Fetch ReccoBeats track info by Spotify track ID.
    Returns the first track in 'content' or None.
    """
    url = f"{BASE_URL}/track?ids={spotify_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching ReccoBeats track:", response.text)
        return None
    
    data = response.json()
    if not data.get("content") or len(data["content"]) == 0:
        return None

    return data["content"][0]["id"] 


def print_reccobeats_track_id(spotify_id):
    track_id = get_reccobeats_track_id(spotify_id)
    print("Reccobeats track id:", track_id)




if __name__ == "__main__":
    spotify_id = get_current_track_id()
    print_reccobeats_track_id(spotify_id)
