from utils.spotipy_utils import *
from core.clustering import cluster_current_playlist_with_reccobeats, print_current_playlist_clusters
from core.transition_engine import TransitionEngine

class BartenderController:
    def __init__(self):
        self.cluster_result = None
        self.engine = None
        self.sequence = None
    
    def _ensure_engine(self):
        if self.engine is None:
            self.cluster_result = cluster_current_playlist_with_reccobeats()
            self.engine = TransitionEngine(self.cluster_result)

    def create_stirred_playlist(self, execute=False):
        self._ensure_engine()

        print("Generating stirred playlist...")
        sequence = self.engine.generate_stirred()

        track_ids = [s["spotify_id"] for s in sequence]

        render_playlist(
            track_ids=track_ids,
            name="Bartender - Stirred",
            description="Smooth transitions",
            public=False,
            execute=execute
        )


    def create_shaken_playlist(self, execute=False):
        self._ensure_engine()

        print("Generating shaken playlist...")
        sequence = self.engine.generate_shaken()

        track_ids = [s["spotify_id"] for s in sequence]

        render_playlist(
            track_ids=track_ids,
            name="Bartender - Shaken",
            description="Chaotic, high-contrast transitions",
            public=False,
            execute=execute
        )

    def run(self):
        actions = {
            "n": ("Next Track ⏭️", next_track),
            "p": ("Previous Track ⏮️", previous_track),
            "pause": ("Pause ⏸️", pause_playback),
            "resume": ("Resume ▶️", resume_playback),
            "song": ("Show Current Track", print_current_playing),
            "pli": ("Show Current Playlist Info", print_current_playlist_info),
            "pls": ("Show Current Playlist Songs", print_current_playlist_tracks_data),
            "cluster": ("Show Current Playlist Clusters", print_current_playlist_clusters),
            "stirred": ("Preview new Stirred Playlist", lambda: self.create_stirred_playlist(execute=False)),
            "shaken": ("Preview new Shaken Playlist", lambda: self.create_shaken_playlist(execute=False)),
            "!stirred": ("Create new Stirred Playlist", lambda: self.create_stirred_playlist(execute=True)),
            "!shaken": ("Create new Shaken Playlist", lambda: self.create_shaken_playlist(execute=True)),
            "p-on": ("Turn on permissions", allow_changes),
            "p-off": ("Turn off permissions", disallow_changes),
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

if __name__ == "__main__":
    controller = BartenderController()
    controller.controller()
