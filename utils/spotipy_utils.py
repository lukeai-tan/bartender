import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

def create_sp(scopes):
    auth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scopes
    )
    return spotipy.Spotify(auth_manager=auth)


def search_track(track_name, artist_name=None, limit=1):
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"

    sp = create_sp("user-top-read user-library-read")

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


def print_track_info(track_info):
    print(f"{track_info['name']} - {track_info['artists']}")
    print(f"Album: {track_info['album']}")
    print(f"Release Date: {track_info['release_date']}")
    print(f"Popularity: {track_info['popularity']}")
    print(f"Spotify URL: {track_info['external_url']}")



def get_current_playing():
    sp = create_sp("user-read-currently-playing user-read-playback-state")
    
    current = sp.current_user_playing_track()

    if not current or current['item'] is None:
        return None  # Nothing is playing

    track = current['item']
    info = {
        "id": track['id'],
        "name": track['name'],
        "artists": ', '.join([a['name'] for a in track['artists']]),
        "album": track['album']['name'],
        "release_date": track['album']['release_date'],
        "popularity": track['popularity'],
        "external_url": track['external_urls']['spotify'],
        "is_playing": current.get("is_playing", False),
        "progress_ms": current.get("progress_ms", 0),
        "duration_ms": track.get("duration_ms", 0),
    }
    return info

def print_current_playing():
    info = get_current_playing()

    if info is None:
        print("🎵 No track is currently playing.")
        return
    
    progress = ms_to_min_sec(info['progress_ms'])
    duration = ms_to_min_sec(info['duration_ms'])

    print("🎶 Now Playing:")
    print(f"  Track:   {info['name']}")
    print(f"  Artist:  {info['artists']}")
    print(f"  Album:   {info['album']}")
    print(f"  URL:     {info['external_url']}")
    print(f"  Playing: {info['is_playing']}")
    print(f"  Progress:  {progress} / {duration}")


def ms_to_min_sec(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"