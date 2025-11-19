# Spotify Utils

Utility functions for interacting with the Spotify Web API using the Spotipy library.  
These helpers allow you to control playback, fetch currently playing information, inspect playlist data, and search tracks.

---

## Configuration

The module loads Spotify credentials from environment variables:

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`

All functions use full permissions defined in `ALL_SCOPES`.

---

## Authentication

### `create_sp()`
Creates and returns an authenticated Spotipy client using OAuth.

**Scopes included:**

- user-read-currently-playing  
- user-read-playback-state  
- user-modify-playback-state  
- user-library-read  
- user-top-read  
- playlist-read-private  

---

## Track Search

### `search_track(track_name, artist_name=None, limit=1)`
Searches Spotify for a track by name and (optionally) artist.

**Returns:**  
A dictionary with:

- `id`
- `name`
- `artists`
- `album`
- `release_date`
- `popularity`
- `external_url`

Or `None` if no match.

---

## Playback Control

### `pause_playback()`
Pauses the current Spotify playback.

### `resume_playback()`
Resumes playback on the active device.

### `next_track()`
Skips to the next track.

### `previous_track()`
Goes back to the previous track.

### `play_track_in_playlist(playlist_id, track_id)`
Starts playing a specific track from a playlist.

---

## Currently Playing

### `get_current_playing()`
Returns metadata about the currently playing track.

Fields include:

| Key | Description |
|-----|-------------|
| id | Track ID |
| name | Track name |
| artists | Artist names |
| album | Album name |
| release_date | Album release date |
| popularity | Spotify popularity (0–100) |
| external_url | Spotify link |
| is_playing | Whether playback is active |
| progress_ms | Current position |
| duration_ms | Track duration |

### `print_current_playing()`
Pretty-prints the currently playing song with timecodes.

---

## Time Formatting

### `ms_to_min_sec(ms)`
Converts milliseconds → `minutes:seconds`.

---

## Playlist Information

### `get_current_playlist_id()`
Returns the playlist ID of the playlist currently being played, or `None`.

### `get_current_playlist()`
Returns the name of the current playlist (if playing from a playlist).

### `print_current_playlist_name()`
Prints the name of the current playlist.

### `get_current_playlist_info()`
Returns a dictionary containing:

- `id`
- `name`
- `owner`
- `url`
- `tracks` (number of tracks)

### `print_current_playlist_info()`
Prints formatted playlist metadata.

---

## Playlist Tracks

### `get_playlist_tracks(playlist_id)`
Fetches **every track** in a playlist (handling pagination).

Returns a list of dictionaries:

| Key | Description |
|-----|-------------|
| id | Track ID |
| name | Track name |
| artists | Artists |
| album | Album name |
| release_date | Release date |
| duration_ms | Duration in milliseconds |
| popularity | Popularity score |
| url | Spotify track link |

### `print_playlist_tracks_data(playlist_id)`
Prints all tracks in the playlist with index, name, artists, and duration.

### `print_current_playlist_tracks_data()`
Prints track data for whichever playlist is currently playing.



