# Spotify Utils

Utility functions for interacting with the **Spotify Web API** using the **Spotipy** library.  
This module provides tools for playback control, playlist management, searching music, and inspecting currently playing data.

---

## Configuration

Credentials are loaded automatically from environment variables:

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`

These must be set before using the module.

Every Spotify client is created with the full permission set:

```
user-read-currently-playing  
user-read-playback-state  
user-modify-playback-state  
user-library-read  
user-top-read  
playlist-read-private  
playlist-modify-private  
playlist-modify-public
```

---

## Authentication

### `create_sp()`
Creates and returns a fully authenticated `spotipy.Spotify` client using OAuth.

Used internally by all other functions.

---

## Safe Mode (Write Protection)

Modifying playlists can be dangerous, so **Safe Mode** is enabled by default.

### `allow_changes()`
Disables Safe Mode.  
Write operations (add/remove/clone playlists) are **allowed**.

### `disallow_changes()`
Enables Safe Mode.  
Write operations are **blocked**.

### `assert_safe_mode()`
Returns `True` if changes are allowed, otherwise prints a warning and blocks the action.

---

## Track Search

### `search_track(track_name, artist_name=None, limit=1)`
Searches Spotify for a track.

#### Returns:
A dictionary:

| Key | Description |
|-----|-------------|
| id | Spotify track ID |
| name | Track name |
| artists | Artist names |
| album | Album name |
| release_date | Album release year |
| popularity | Popularity (0–100) |
| external_url | Spotify URL |

Returns `None` if no results.

### `print_track_info(track_info)`
Pretty-prints the dictionary from `search_track()`.

---

## Currently Playing

### `get_current_playing()`
Returns metadata about the currently playing track, or `None`.

#### Returned dictionary fields:
| Key | Description |
|-----|-------------|
| id | Track ID |
| name | Track name |
| artists | Artist(s) |
| album | Album |
| release_date | Album release date |
| popularity | Spotify popularity |
| external_url | Track link |
| is_playing | True/False |
| progress_ms | Playback position |
| duration_ms | Total duration |

### `print_current_playing()`
Prints a formatted "Now Playing" display with song info and timecodes.

### `get_current_track_id()`
Returns ID of the currently playing track.

### `print_current_track_id()`
Prints the current track ID.

---

## Playback Control

### `pause_playback()`
Pauses the current device.

### `resume_playback()`
Resumes playback.

### `next_track()`
Skips to the next track.

### `previous_track()`
Returns to the previous track.

---

## Playlist Identification

### `get_current_playlist_id()`
Returns the playlist ID being listened to, or `None` if not listening from a playlist.

### `get_current_playlist()`
Returns the current playlist name, if applicable.

### `print_current_playlist_name()`
Prints the name of the playlist you're currently listening to.

---

## Playlist Info

### `get_current_playlist_info()`
Returns metadata for the playlist currently being listened to.

Returned dictionary:

| Key | Description |
|-----|-------------|
| id | Playlist ID |
| name | Playlist name |
| owner | Owner username |
| url | Spotify URL |
| tracks | Number of tracks |

### `print_current_playlist_info()`
Pretty-prints playlist metadata.

---

## Playlist Tracks

### `get_playlist_tracks(playlist_id)`
Returns **all tracks** in a playlist, including pagination.

Each track is returned as:

| Key | Description |
|-----|-------------|
| id | Track ID |
| name | Track name |
| artists | Artist names |
| album | Album |
| release_date | Release date |
| duration_ms | Duration |
| popularity | Popularity score |
| url | Spotify link |

### `print_playlist_tracks_data(playlist_id)`
Prints all tracks with numbering + formatted duration.

### `print_current_playlist_tracks_data()`
Prints tracklist for whatever playlist is currently playing.

---

## Playlist Modification

> **Note:** All operations are blocked unless Safe Mode is disabled using `allow_changes()`.

### `clone_playlist(source_playlist_id, new_name=None, execute=False)`
Creates a full duplicate of a playlist.

Parameters:

| Parameter | Description |
|----------|-------------|
| source_playlist_id | Playlist to clone |
| new_name | Optional name for new playlist |
| execute | If `False`: Dry-run (no changes) |

Returns: new playlist ID or `None`.

### `add_track_to_playlist(playlist_id, track_id, execute=False)`
Adds a track to a playlist (requires Safe Mode OFF).

### `remove_track_from_playlist(playlist_id, track_id, execute=False)`
Removes a specific track from a playlist (requires Safe Mode OFF).

---

## Audio Features (Local Printer)

### `print_audio_features(features)`
Pretty-prints a dictionary of audio features.

Expected fields:

- acousticness  
- danceability  
- energy  
- instrumentalness  
- liveness  
- loudness  
- speechiness  
- valence  
- tempo  
- key *(optional)*  
- mode *(optional)*  
- time_signature *(optional)*  

If the dict is empty or `None`, prints a fallback message.


