from core.clustering import ClusterResult, cluster_current_playlist_with_reccobeats
from utils.spotipy_utils import render_playlist, allow_changes
import numpy as np
import random

class TransitionEngine:
    def __init__(self, cluster_result):
        self.result = cluster_result
        self.df = cluster_result.df
        self.X = cluster_result.X_scaled
        self.model = cluster_result.model
        self.clusters = cluster_result.clusters
        self.song_to_cluster = self._build_song_cluster_map()
    
    def _centroid(self, cid):
        return self.model.cluster_centers_[cid]

    def _cluster_distance(self, c1, c2):
        a = self._centroid(c1)
        b = self._centroid(c2)
        return np.linalg.norm(a - b)

    # Find closest track to a vector
    def _closest_song_to_vector(self, vec):
        distances = np.linalg.norm(self.X - vec, axis=1)
        idx = distances.argmin()
        return self.df.iloc[idx]
    
    def _order_clusters(self, mode="nearest"):
        """
        Order clusters using a greedy heuristic on centroid distances.

        mode:
            - "nearest"  : Nearest Neighbour
            - "furthest" : Furthest Neighbour
        """
        k = len(self.clusters)

        unvisited = set(range(k))
        path = []

        current = 0 # start with 0 for now
        path.append(current)
        unvisited.remove(current)

        if mode == "nearest":
            chooser = min
        elif mode == "farthest":
            chooser = max
        else:
            raise ValueError(f"Unknown ordering mode: {mode}")

        while unvisited:
            next_c = chooser(
                unvisited,
                key=lambda c: self._cluster_distance(current, c)
            )
            path.append(next_c)
            unvisited.remove(next_c)
            current = next_c

        return path

    def _append_cluster_songs(self, cid, sequence, used_song_ids):
        """
        Append all songs from a cluster to sequence,
        avoiding duplicates.
        """
        for idx in self.clusters[cid]:
            row = self.df.iloc[idx]
            sid = row["spotify_id"]

            if sid not in used_song_ids:
                sequence.append(row.to_dict())
                used_song_ids.add(sid)


    def _append_song(self, sequence, used_song_ids, idx):
        used_song_ids.add(idx)
        sequence.append(self.df.iloc[idx].to_dict())


    def _find_midpoint_song(self, a, b):
        """
        Find the song closest to the midpoint between
        cluster a and cluster b centroids.
        """
        centroid_a = self._centroid(a)
        centroid_b = self._centroid(b)

        midpoint = (centroid_a + centroid_b) / 2
        return self._closest_song_to_vector(midpoint)


    def _build_song_cluster_map(self):
        song_to_cluster = {}
        for cid, indices in self.clusters.items():
            for idx in indices:
                song_to_cluster[idx] = cid
        return song_to_cluster


    def _farthest_song(self, from_idx, candidates):
        from_vec = self.X[from_idx]
        return max(
            candidates,
            key=lambda idx: np.linalg.norm(self.X[idx] - from_vec)
        )

    def _get_shaken_candidates(self, current_cluster, used_song_ids, intra_prob):
        if random.random() < intra_prob:
            candidates = [
                idx for idx in self.clusters[current_cluster]
                if idx not in used_song_ids
            ]
            if candidates:
                return candidates

        return [
            idx for idx in range(len(self.df))
            if idx not in used_song_ids and self.song_to_cluster[idx] != current_cluster
        ]


    def generate_stirred(self):
        """
        Smooth transitions:
        - Order clusters by nearest-neighbour heuristic
        - Dump cluster songs in order
        - Insert midpoint songs between clusters
        """
        path = self._order_clusters(mode="nearest")

        sequence = []
        used_song_ids = set()

        # Walk cluster path
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]

            # Dump current cluster
            self._append_cluster_songs(a, sequence, used_song_ids)

            # Insert midpoint transition
            mid_song = self._find_midpoint_song(a, b)
            sid = mid_song["spotify_id"]

            if sid not in used_song_ids:
                sequence.append(mid_song.to_dict())
                used_song_ids.add(sid)

        # Dump last cluster
        self._append_cluster_songs(path[-1], sequence, used_song_ids)

        return sequence


    def generate_shaken(self, intra_prob=0.7):
        n = len(self.df)
        used_song_ids = set()

        current_idx = random.randrange(n)
        sequence = []
        self._append_song(sequence, used_song_ids, current_idx)

        current_cluster = self.song_to_cluster[current_idx]

        while len(used_song_ids) < n:
            candidates = self._get_shaken_candidates(
                current_cluster, used_song_ids, intra_prob
            )

            if not candidates:
                candidates = [
                    idx for idx in range(len(self.df))
                    if idx not in used_song_ids
                ]
                if not candidates:
                    break

            next_idx = self._farthest_song(current_idx, candidates)

            self._append_song(sequence, used_song_ids, next_idx)

            current_idx = next_idx
            current_cluster = self.song_to_cluster[current_idx]

        return sequence


    def generate(self, mode="stirred"):
        if mode == "stirred":
            return self.generate_stirred()
        elif mode == "shaken":
            return self.generate_shaken()
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    def debug_print_sequence(self, sequence):
        print("\n=== GENERATED SEQUENCE ===")
        for i, track in enumerate(sequence):
            print(f"{i+1:02d}. {track['name']} - {track['artists']}  ({track['spotify_id']})")



if __name__ == "__main__":
    #print_current_playlist_clusters()
    
    cluster_result:ClusterResult = cluster_current_playlist_with_reccobeats()
    engine = TransitionEngine(cluster_result=cluster_result)
    sequence = engine.generate_shaken()
    track_ids = [s["spotify_id"] for s in sequence]
    allow_changes()
    render_playlist(
        track_ids,
        name="Bartender - Shaken",
        description="Experimental Shaken Mode",
        execute=True
    )

