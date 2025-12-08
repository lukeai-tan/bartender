import os
import pandas as pd
from utils.reccobeats_utils import get_reccobeats_audio_features_with_spotify_id
from utils.spotipy_utils import get_playlist_tracks

AUDIO_FEATURE_KEYS = [
    "danceability", 
    "energy", 
    "loudness", 
    "speechiness",
    "acousticness", 
    "instrumentalness", 
    "liveness",
    "valence", 
    "tempo"
]

CACHE_DIR = "data/playlist_cache"


def ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def load_cached_playlist(playlist_id):
    """Return a DataFrame if cache exists, else None."""
    ensure_cache_dir()
    path = f"{CACHE_DIR}/{playlist_id}.csv"
    return pd.read_csv(path) if os.path.exists(path) else None


def save_playlist_cache(playlist_id, df):
    ensure_cache_dir()
    path = f"{CACHE_DIR}/{playlist_id}.csv"
    df.to_csv(path, index=False)


def fetch_and_cache_playlist(playlist_id):
    """
    Returns a DataFrame.
    If cache exists → load.
    If not → fetch from APIs and create CSV.
    """

    cached = load_cached_playlist(playlist_id)
    if cached is not None:
        print(f"📁 Loaded cached playlist: {playlist_id}")
        return cached

    print(f"🔍 Fetching fresh data for playlist: {playlist_id}")

    tracks = get_playlist_tracks(playlist_id)
    rows = []

    for t in tracks:
        sid = t["id"]

        audio = get_reccobeats_audio_features_with_spotify_id(sid)
        if not audio:
            continue

        row = {
            "spotify_id": sid,
            "name": t["name"],
            "artists": t["artists"],
        }

        for key in AUDIO_FEATURE_KEYS:
            row[key] = audio[key]

        rows.append(row)

    df = pd.DataFrame(rows)
    save_playlist_cache(playlist_id, df)

    print(f"💾 Cached playlist to CSV ({len(df)} tracks)")

    return df
