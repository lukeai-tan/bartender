import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")


ALL_SCOPES = (
    "user-read-currently-playing "
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-library-read "
    "user-top-read "
    "playlist-read-private "
)


def create_sp():
    auth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=ALL_SCOPES,
    )
    return spotipy.Spotify(auth_manager=auth)


def search_track(track_name, artist_name=None, limit=1):
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"

    sp = create_sp()

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


'''
Methods to get account specific data
'''

def get_current_playing():
    sp = create_sp()
    
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


def pause_playback():
    sp = create_sp()
    try:
        sp.pause_playback()
        print("⏸️ Playback paused.")
    except Exception as e:
        print("Error pausing playback:", e)


def resume_playback():
    sp = create_sp()
    try:
        sp.start_playback()
        print("▶️ Playback resumed.")
    except Exception as e:
        print("Error resuming playback:", e)


def next_track():
    sp = create_sp()
    try:
        sp.next_track()
        print("⏭️ Skipped to next track.")
    except Exception as e:
        print("Error skipping track:", e)


def previous_track():
    sp = create_sp()
    try:
        sp.previous_track()
        print("⏮️ Went to previous track.")
    except Exception as e:
        print("Error going to previous track:", e)


def play_track_in_playlist(playlist_id, track_id):
    sp = create_sp()
    sp.start_playback(
        context_uri=f"spotify:playlist:{playlist_id}",
        offset={"uri": f"spotify:track:{track_id}"}
    )
    print("Now playing track:", track_id)


def get_current_playlist_id():
    sp = create_sp()

    current = sp.current_user_playing_track()

    if not current:
        return None

    context = current.get("context")

    # Must be coming from a playlist
    if not context or context.get("type") != "playlist":
        return None

    uri = context.get("uri")
    if not uri:
        return None

    playlist_id = uri.split(":")[-1]
    return playlist_id


def get_current_playlist():
    sp = create_sp()
    current = sp.current_user_playing_track()
    if not current:
        return None

    context = current.get("context")
    if context and context["type"] == "playlist":
        playlist_uri = context["uri"]
        playlist = sp.playlist(playlist_uri)
        return playlist["name"]
    return None


def print_current_playlist_name():
    playlist_name = get_current_playlist()
    if playlist_name:
        print(f"🎶 Current Playlist: {playlist_name}")
    else:
        print("🎵 Not playing from a playlist.")


def get_current_playlist_info():
    sp = create_sp()
    current = sp.current_user_playing_track()

    if not current:
        return None

    context = current.get("context")

    if not context or context.get("type") != "playlist":
        return None

    playlist_uri = context.get("uri")
    playlist_id = playlist_uri.split(":")[-1]

    playlist = sp.playlist(playlist_id)

    return {
        "id": playlist_id,
        "name": playlist["name"],
        "owner": playlist["owner"]["display_name"],
        "url": playlist["external_urls"]["spotify"],
        "tracks": playlist["tracks"]["total"]
    }


def print_current_playlist_info():
    info = get_current_playlist_info()

    if not info:
        print("🎵 Not currently playing from a playlist.")
        return

    print("\nCurrent Playlist Info")
    print("────────────────────────────────")
    print(f"Name:   {info['name']}")
    print(f"Owner:  {info['owner']}")
    print(f"Tracks: {info['tracks']}")
    print(f"ID:     {info['id']}")
    print(f"URL:    {info['url']}")
    print("────────────────────────────────")


def get_playlist_tracks(playlist_id):
    sp = create_sp()

    results = sp.playlist_items(playlist_id, limit=100)
    tracks = results["items"]

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    playlist_data = []

    for item in tracks:
        track = item["track"]
        if track is None:
            continue

        playlist_data.append({
            "id": track["id"],
            "name": track["name"],
            "artists": ", ".join(a["name"] for a in track["artists"]),
            "album": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "duration_ms": track["duration_ms"],
            "popularity": track["popularity"],
            "url": track["external_urls"]["spotify"]
        })

    return playlist_data


def print_playlist_tracks_data(playlist_id):
    sp = create_sp()
    playlist = sp.playlist(playlist_id)

    print(f"\n🎵 Playlist: {playlist['name']}")
    print(f"Tracks: {playlist['tracks']['total']}\n")

    tracks = get_playlist_tracks(playlist_id)

    for i, t in enumerate(tracks, start=1):
        minutes = t["duration_ms"] // 60000
        seconds = (t["duration_ms"] // 1000) % 60

        print(f"{i}. {t['name']} — {t['artists']} ({minutes}:{seconds:02d})")


def print_current_playlist_tracks_data():
    playlist_id = get_current_playlist_id()

    if not playlist_id:
        print("🎵 No playlist is currently playing.")
        return

    print_playlist_tracks_data(playlist_id)


if __name__ == "__main__":
    print_current_playlist_info()
