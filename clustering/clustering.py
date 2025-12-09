from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from utils.spotipy_utils import *
from utils.caching_utils import fetch_and_cache_playlist, AUDIO_FEATURE_KEYS


class ClusterResult:
    def __init__(self, clusters, df, model, X_scaled, scaler):
        self.clusters = clusters          # dict: cid → [song labels]
        self.df = df                      # original DataFrame
        self.model = model                # trained KMeans model
        self.X_scaled = X_scaled          # scaled feature matrix
        self.scaler = scaler              # fitted StandardScaler


def cluster_playlist_with_reccobeats(playlist_id, k=None):
    df = fetch_and_cache_playlist(playlist_id)

    # features matrix
    X = df[AUDIO_FEATURE_KEYS].to_numpy()

    # scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # auto-k
    if k is None:
        best_k = None
        best_score = -1

        for test_k in range(2, min(10, len(X_scaled))):
            km = KMeans(n_clusters=test_k, random_state=42)
            cluster_labels = km.fit_predict(X_scaled)
            score = silhouette_score(X_scaled, cluster_labels)

            if score > best_score:
                best_score = score
                best_k = test_k

        k = best_k
        print(f"\n📐 Auto-selected best k = {k} (silhouette: {best_score:.3f})")


    # final model
    model = KMeans(n_clusters=k, random_state=42)
    cluster_ids = model.fit_predict(X_scaled)

    # build dictionary
    clusters = {cid: [] for cid in range(k)}

    for (_, row), cid in zip(df.iterrows(), cluster_ids):
        label = f"{row['name']} — {row['artists']}"
        clusters[cid].append(label)

    return ClusterResult(
        clusters=clusters,
        df=df,
        model=model,
        X_scaled=X_scaled,
        scaler=scaler
    )


def print_clusters(cluster_result: ClusterResult):
    clusters = cluster_result.clusters

    print(f"\n🍸 Clusters (k={len(clusters)})")
    print("─────────────────────────────────────")

    for cid, songs in clusters.items():
        print(f"\n🍹 Cluster {cid + 1} - Flavor Profile")
        print("──────────────────────────────")
        for s in songs:
            print(f"• {s}")
        

def cluster_current_playlist_with_reccobeats():
    playlist_id = get_current_playlist_id()
    cluster_result: ClusterResult = cluster_playlist_with_reccobeats(playlist_id=playlist_id)
    return cluster_result


def print_current_playlist_clusters():
    cluster_result: ClusterResult = cluster_current_playlist_with_reccobeats()
    print_clusters(cluster_result=cluster_result)


if __name__ == "__main__":
    print_current_playlist_clusters()
