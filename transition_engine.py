from clustering.clustering import *
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

    def generate_stirred(self):
        """
        Smooth transitions:
        - Follow clusters in order of centroid proximity
        - Insert midpoint songs between clusters
        - Final output is a smooth-flowing playlist
        """
        pass

    def generate_shaken(self):
        """
        Chaotic but fun transitions:
        - Jump across clusters
        - Ensure high audio contrast
        - Still avoids completely random noise
        """
        pass
    
    def generate(self, mode="stirred"):
        if mode == "stirred":
            return self.generate_stirred()
        elif mode == "shaken":
            return self.generate_shaken()
        else:
            raise ValueError(f"Unknown mode: {mode}")
   


if __name__ == "__main__":
    print_current_playlist_clusters()