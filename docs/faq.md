# FAQ
## What's the difference between Stirred and Shaken?
Stirred prioritises smoothness and gradual transitions between similar songs and clusters.\
Shaken maximises contrast, jumping between distant songs and clusters to create surprise and greater entropy.

Both modes use the same underlying audio features but apply different traversal techniques.

## Why don't transitions involve actual audio crossfades or beat matching?
That was actually the original concept for Bartender. Unfortunately, Spotify's Web API doesn't allow access to the raw audio or playback buffers. Bartender only operates at the playlist sequencing level, not the audio processing level.

## Can songs repeat or be skipped?
The transition engine tracks which songs have already been used to avoid duplicates. If missing songs occur, it's usually because the Reccobeat API cannot recognise the Spotify song, and is thus unable to fetch its audio features for the clustering.

## Why use K-Means clustering?
K-Means is fast, interpretable and works well for low-dimensional numeric feature spaces like Spotify audio features. Also, since playlist sizes are relatively small (approx 200?), the time complexity of K-Means is pretty effificient.

## Is this meant to be a real DJ replacement?
Nope, it's more of an algorithmic mixtape, cocktail if you will.
