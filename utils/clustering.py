import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from reccobeats_utils import (
    get_reccobeats_track_data,
    get_reccobeats_audio_features
)
from spotipy_utils import *


AUDIO_FEATURE_KEYS = [
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]


def cluster_playlist_with_reccobeats(playlist_id, k=None):
    """
    Cluster a Spotify playlist using ReccoBeats audio features.

    k = None → automatically finds best k using silhouette score.
    """

    playlist_tracks = get_playlist_tracks(playlist_id)

    all_features = []
    labels = []

    for track in playlist_tracks:
        spotify_id = track["id"]

        # Get ReccoBeats track entry
        track_data = get_reccobeats_track_data(spotify_id)
        if not track_data:
            continue

        recco_id = track_data["id"]

        # Get audio features
        features = get_reccobeats_audio_features(recco_id)
        if not features:
            continue

        try:
            vector = [features[key] for key in AUDIO_FEATURE_KEYS]
        except KeyError:
            continue

        all_features.append(vector)
        labels.append(f"{track['name']} — {track['artists']}")

    # Convert to numpy array
    X = np.array(all_features)

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Auto-k mode
    if k is None:
        best_k = None
        best_score = -1
        possible = range(2, min(10, len(X_scaled)))

        for test_k in possible:
            km = KMeans(n_clusters=test_k, random_state=42)
            clusters = km.fit_predict(X_scaled)
            score = silhouette_score(X_scaled, clusters)

            if score > best_score:
                best_k = test_k
                best_score = score

        k = best_k
        print(f"\n📐 Auto-selected best k = {k} (silhouette: {best_score:.3f})")

    # Final clustering
    model = KMeans(n_clusters=k, random_state=42)
    cluster_ids = model.fit_predict(X_scaled)

    # Print output bartender style
    print(f"\n🍸 Clusters (k={k})")
    print("─────────────────────────────────────")

    clusters = {i: [] for i in range(k)}

    for label, cid in zip(labels, cluster_ids):
        clusters[cid].append(label)

    for cid, songs in clusters.items():
        print(f"\n🍹 Cluster {cid + 1} - Flavor Profile")
        print("──────────────────────────────")
        for s in songs:
            print(f"• {s}")

    return clusters


if __name__ == "__main__":
    playlist_id = get_current_playlist_id()
    cluster_playlist_with_reccobeats(playlist_id=playlist_id)