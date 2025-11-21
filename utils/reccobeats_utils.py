import requests
from spotipy_utils import *

BASE_URL = "https://api.reccobeats.com/v1"


def get_reccobeats_track_data(spotify_id):
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

    return data["content"][0]


def get_reccobeats_track_id(spotify_id):
    track_data = get_reccobeats_track_data(spotify_id)
    return track_data["id"]


def print_reccobeats_track_id(spotify_id):
    track_id = get_reccobeats_track_id(spotify_id)
    print("Reccobeats track id:", track_id)


def print_reccobeats_track_title(spotify_id):
    track_data = get_reccobeats_track_data(spotify_id)
    track_title = track_data["trackTitle"]
    print("Track Title:", track_title)


def get_reccobeats_audio_features(track_id):
    """Fetch ReccoBeats audio features for a ReccoBeats track ID."""
    url = f"{BASE_URL}/track/{track_id}/audio-features"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching audio features:", response.text)
        return None

    return response.json()


def print_reccobeats_audio_features(spotify_id):
    """Fetch and print audio features for a Spotify track via ReccoBeats."""
    # convert Spotify URI to just the ID if needed
    if spotify_id.startswith("spotify:track:"):
        spotify_id = spotify_id.split(":")[-1]

    # get the ReccoBeats track ID
    url = f"{BASE_URL}/track?ids={spotify_id}"
    response = requests.get(url)
    if response.status_code != 200 or not response.json().get("content"):
        print("Track not found in ReccoBeats.")
        return

    recco_id = response.json()["content"][0]["id"]

    # fetch audio features
    features = get_reccobeats_audio_features(recco_id)
    if not features:
        print("No audio features available.")
        return

    print("\nReccoBeats Audio Features")
    print("──────────────────────────────")
    for key, value in features.items():
        if key in ["id", "href"]:
            continue
        print(f"{key.capitalize():20}: {value}")
    print("──────────────────────────────\n")


if __name__ == "__main__":
    spotify_id = get_current_track_id()
    print_reccobeats_track_title(spotify_id)
    print_reccobeats_audio_features(spotify_id)
