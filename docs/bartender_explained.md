# How Bartender Works

## Why I Built This Transition Engine
When I add songs on spotify, I tend to just toss in any song I was interested in at that point in time into my main playlist. In 2024, I got really into J-POP, so I added a bunch of J-POP classics into the mix. Fast forward into 2025, Expedition 33 and Hollow Knight: SilkSong came out, and of course I dumped the soundtracks' greatest hits into there. 

As you can probably tell, the huge difference in genres that make up my playlist has consequently made it into a mess. I tried using the shuffle feature to spread out my tracks evenly but I felt that it wasn't really working. 

I realised what I needed was something that could strategically organise my songs such that I wouldn't get whiplash when the tracks switched from a calm OST to a sudden high BPM boss fight OST.

## Explaining Bartender
I chose the theme Bartender because I envisioned a bartender shaking up and mixing drinks, or rather songs, and then serving them as one playlist. It also kind of works out because of the play on words "bar" and "tender", like bars of a song. I am very funny.

The core functionality of Bartender can be broken down into these steps:

1. Analyse your playlist songs
2. Cluster them by audio features
3. Rearrange the songs with a transition algorithm
4. Spit out the new playlist (voilà)

The playlist is intended to be played in the given order, so you won't see any difference if you play it on shuffle or magic shuffle.

## Explaining Clustering
The clustering algorithm is quite simple. First, I utilised the Spotify Web API to fetch all the songs in the playlist. I then used Reccobeats to fetch their individual audio features, and convert them into column vectors. Using K-means Clustering, I split the playlist up into k clusters, with each cluster having songs with similar patterns or audio features. 

## Introducing the two transition modes: Stirred vs Shaken
My inspiration for the transition modes came from the iconic catchphrase "Shaken, not stirred" from James Bond. I don't know what it means nor have I watched James Bond.

### Stirred Mode
The Stirred mode is designed to simulate a smooth pour kind of transition.
The idea is simple:
songs that sound similar should play close together, and transitions between different "flavours" of music should be more natural rather than abrupt.

#### Step 1: Cluster the playlist
First, the playlist is clustered using audio features such as energy, tempo, valence, and danceability.
Each cluster represents a flavor profile, which is what I call a group of songs that are already musically similar.
Since songs within a cluster are close to each other in feature space, playing them consecutively already produces a smooth listening experience.

#### Step 2: Order clusters by similarity
Stirred mode determines the order in which clusters should be played. Starting from an initial cluster, the algorithm repeatedly selects the nearest unvisited cluster, based on the distance between the cluster centroids. This is done using a greedy nearest-neighbour heuristic. This results in an ordering where each cluster transition is as smooth as possible

#### Step 3: Insert a midpoint transition song
To further soften transitions between clusters, Stirred mode introduced a midpoint song.

For each transition from cluster A to B:

1. Draw a line between the centroids of cluster A and B

2. Compute the midpoint M of that line

3. Find the sond whose audio feature vector is closest to M

This midpoint song acts like a bridge between clusters, where it theoretically shares characteristics of both clusters and helps ease the listener into the next flavour.

#### Step 4: Assemble the final playlist
The final playlist is constructed as:

- All songs from cluster A
- A midpoint transition song
- All songs from cluster B
- Repeat until all clusters are visited


### Shaken Mode
The Shaken mode is the complete opposite.
Instead of minimising distance between transitions, it maximises contrast.
While Stirred mode's agenda is "What comes next most smoothly?", Shaken mode's agenda is "What would feel the most surprising right now?"

In this mode:

- Songs frequently jump across distant clusters
- Transitions are intentionally energetic
- The playlist is unpredictable

However, despite the chaos, Shaken mode is still controlled, where transitions are driven by audio feature distances rather than pure randomness alone.

#### Step 1: Choose a random starting song
Shaken mode begins by selecting a random song from the playlist. This track becomes the starting point of the sequence and sets the stage for the initial musical context.

#### Step 2: Decide jump type (controlled chaos)
At each step, the algorithm decides how the next song should be chosen. A random number n from 0 to 1 is drawn.

With probability p (default 0.7):

- It attempts an intra-cluster jump, staying within the same flavour profile
- Considers only unused songs from the current cluster

With probability 1 - p (default 0.3):

- It forces an inter-cluster jump, moving to a completely differenet flavour profile.
- Considers only unused songs from songs from all other clusters

If no valid intra-cluster songs remain, the algorithm automatically falls back to an inter-cluster jump. Same for vice versa.

This balance prevents the playlist from being either too smooth or completely chaotic.

#### Step 3: Maximise contrast
Shaken mode selects the song that is fartest away from the current song in the feature space. This ensures that each transition introduces a maxmimum contrast.

#### Step 4: Repeat until all songs are used
The algorithm repeats this process, selecting the farthest valid song at each step, be it intra or inter-cluster, until every song in the playlist has been used exactly once.

The final result is a playlist that constantly keeps the listener on edge. 


## Conclusion
Now, I can't say for sure whether these stirred or shaken transitions, defined purely by audio features, truly translate into their equivalent transitions when experienced by a human listener.

Music perception is subjective and while the distance in audio feature space is a useful approximation for similarity and contrast, it probably doesn't fully capture the emotional context, or the narrative or taste the listener builds up over time, or whatever it is.

Anyway, Bartender's original intention was never about finding a perfect transition. It was more of a passion project of mine to explore whether I could utilise simple geometric and clustering concepts to shape a playlist in a way that feels intentional instead of random. 
