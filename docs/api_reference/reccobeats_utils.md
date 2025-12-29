# ReccoBeats Utils

Utility functions for interacting with the **ReccoBeats API**.  
These helpers fetch track info and audio features using a Spotify track ID.

---

## Configuration

- Base API URL: `https://api.reccobeats.com/v1`
- Requires the `requests` library.
- Can be used alongside `spotipy_utils` for Spotify integration.

---

## Track Data

### `get_reccobeats_track_data(spotify_id)`
Fetches ReccoBeats track info for a given Spotify track ID.

**Returns:**  
A dictionary representing the first track in the ReccoBeats `content` list, or `None` if not found.

**Example fields returned:**

- `id` – ReccoBeats track ID  
- `trackTitle` – Track title  
- `artists` – List of artist objects  
- `durationMs` – Track duration in milliseconds  
- `href` – Spotify track link  
- `popularity` – Track popularity  

---

### `get_reccobeats_track_id(spotify_id)`
Returns the **ReccoBeats track ID** for a given Spotify track ID.  

---

### `print_reccobeats_track_id(spotify_id)`
Fetches and prints the ReccoBeats track ID.

**Example output:**
```
ReccoBeats track id: de5f8816-bde0-4123-9cdd-b0b13d921386
```

---

### `print_reccobeats_track_title(spotify_id)`
Prints the track title from ReccoBeats for a given Spotify track ID.

**Example output:**
```
Track Title: Do I Wanna Know?
```

---

## Audio Features

### `get_reccobeats_audio_features(track_id)`
Fetches **audio features** for a ReccoBeats track ID.

**Returns:**  
A dictionary with keys like:

- `acousticness`  
- `danceability`  
- `energy`  
- `instrumentalness`  
- `liveness`  
- `loudness`  
- `speechiness`  
- `valence`  
- `tempo`  
- `key`  
- `mode`  

---

### `print_reccobeats_audio_features(spotify_id)`
Fetches and prints audio features for a Spotify track ID by internally resolving the ReccoBeats ID.

**Example output:**
```
ReccoBeats Audio Features
──────────────────────────────
Acousticness : 0.186
Danceability : 0.548
Energy : 0.532
Instrumentalness : 0.000263
Liveness : 0.217
Loudness : -7.596
Speechiness : 0.0323
Valence : 0.405
Tempo : 85.03
Key : 5
Mode : 1
──────────────────────────────
```

---

## Usage Example

```python
from reccobeats_utils import *

spotify_id = "1jEBSDN5vYViJQr78W7jr2"

# Print ReccoBeats track info
print_reccobeats_track_id(spotify_id)
print_reccobeats_track_title(spotify_id)

# Print audio features
print_reccobeats_audio_features(spotify_id)
```