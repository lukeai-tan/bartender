from utils.spotipy_utils import search_track, print_current_playing, print_track_info
from utils.rapidapi_utils import print_audio_features

# Edit these

def query_song(track_name, artist_name):
    track_name = "Blinding Lights"
    artist_name = "The Weeknd"

    query = f"track:{track_name} artist:{artist_name}"

    track_info = search_track(track_name, artist_name)

    if track_info is None:
        print("Track not found")

    else:
        print_track_info(track_info)
        print_audio_features(track_name, artist_name)


print_current_playing()