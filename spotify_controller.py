from utils.spotipy_utils import *
from utils.rapidapi_utils import print_audio_features

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


def controller():
    actions = {
        "n": ("Next Track ⏭️", next_track),
        "p": ("Previous Track ⏮️", previous_track),
        "pause": ("Pause ⏸️", pause_playback),
        "resume": ("Resume ▶️", resume_playback),
        "song": ("Show Current Track", print_current_playing),
        "playlist": ("Show Current Playlist", print_current_playlist),
        "q": ("Quit", None)
    }

    while True:
        print("\nSpotify Controller")
        for key, (desc, _) in actions.items():
            print(f"[{key}] {desc}")
        
        choice = input("Choose an action: ").lower()
        
        if choice == "q":
            print("Exiting controller.")
            break
        
        action = actions.get(choice)
        if action:
            try:
                action[1]()
            except Exception as e:
                print("Error:", e)
        else:
            print("Invalid choice, try again.")

controller()