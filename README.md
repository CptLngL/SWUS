# SWUS
This is a multiplayer, client-server simulator of the Star Wars Unlimited TCG card game (or, it eventually will be).
I'm doing the implementation in Python using Pygame for the client. 
This is just for educational purposes, I wouldn't seriously advise to use Pygame, nor Python, for a game client, but hey I was curious to learn it and see if I could do it.
If you're looking for an actual playable implementation of SWU there's a couple of web-based versions that will be more easier to use (and already operational and fully-featured).

## Getting the data 
Run SWUS_get_data first. This will grab all the card data and images from one of the main SWU db site on the internet and save to the data/ folder.
This is required for the simulator to work.
Expect about 1gb of data to be downloaded.
