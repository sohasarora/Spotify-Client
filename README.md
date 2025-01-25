This Python code defines a basic Spotify client using Flask. Here's what it does step by step:

Key Features: 
1. Authentication
- Users log in to their Spotify account via the /login route.
- Spotify redirects users back to the app with an authorization code at /callback.
- The app exchanges the authorization code for an access token, stored in the session.
  
2. Fetching Playlists
- Authenticated users can view their playlists at /playlists.
- Each playlist displays its name and a link to play it.

3. Playback
- Users can start playing a playlist by clicking the "Play" link, which hits the /play/<playlist_uri> route.
- The /play/<playlist_uri> endpoint sends a request to Spotify's API to initiate playback.
