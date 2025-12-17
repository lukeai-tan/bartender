from clustering.clustering import ClusterResult, cluster_current_playlist_with_reccobeats
import numpy as np

class TransitionEngine:
    def __init__(self, cluster_result):
        self.result = cluster_result
        self.df = cluster_result.df
        self.X = cluster_result.X_scaled
        self.model = cluster_result.model
        self.clusters = cluster_result.clusters
    
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
            - "nearest"  : smooth transitions (stirred)
            - "furthest" : high contrast transitions (shaken)
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

    def _append_cluster_songs(self, cid, final_sequence, used_song_ids):
        """
        Append all songs from a cluster to final_sequence,
        avoiding duplicates.
        """
        for idx in self.clusters[cid]:
            row = self.df.iloc[idx]
            sid = row["spotify_id"]

            if sid not in used_song_ids:
                final_sequence.append(row.to_dict())
                used_song_ids.add(sid)


    def _find_midpoint_song(self, a, b):
        """
        Find the song closest to the midpoint between
        cluster a and cluster b centroids.
        """
        centroid_a = self._centroid(a)
        centroid_b = self._centroid(b)

        midpoint = (centroid_a + centroid_b) / 2
        return self._closest_song_to_vector(midpoint)


    def generate_stirred(self):
        """
        Smooth transitions:
        - Order clusters by nearest-neighbour heuristic
        - Dump cluster songs in order
        - Insert midpoint songs between clusters
        """
        path = self._order_clusters(mode="nearest")

        final_sequence = []
        used_song_ids = set()

        # Walk cluster path
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]

            # Dump current cluster
            self._append_cluster_songs(a, final_sequence, used_song_ids)

            # Insert midpoint transition
            mid_song = self._find_midpoint_song(a, b)
            sid = mid_song["spotify_id"]

            if sid not in used_song_ids:
                final_sequence.append(mid_song.to_dict())
                used_song_ids.add(sid)

        # Dump last cluster
        self._append_cluster_songs(path[-1], final_sequence, used_song_ids)

        return final_sequence


    def generate_shaken(self):
        """
        High-contrast transitions:
        - Order clusters by farthest-neighbour heuristic
        - Dump cluster songs with no midpoint smoothing
        - Produces energetic and punchy transitions
        """
        path = self._order_clusters(mode="farthest")

        final_sequence = []
        used_song_ids = set()

        for cid in path:
            self._append_cluster_songs(cid, final_sequence, used_song_ids)

        return final_sequence


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
    engine.debug_print_sequence(sequence)
