import requests
from flask import Flask, request, redirect, session, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

CLIENT_ID = 'your_spotify_client_id'  # Replace with your Spotify Client ID
CLIENT_SECRET = 'your_spotify_client_secret'  # Replace with your Spotify Client Secret
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPES = 'user-read-private playlist-read-private user-modify-playback-state'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'

@app.route('/')
def index():
    return '<a href="/login">Login to Spotify</a>'

@app.route('/login')
def login():
    auth_url = (f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri="
                f"{REDIRECT_URI}&scope={SCOPES}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()
    session['access_token'] = token_json.get('access_token')
    return redirect('/playlists')

@app.route('/playlists')
def playlists():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/')

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f"{API_BASE_URL}/me/playlists", headers=headers)
    playlists = response.json().get('items', [])

    playlist_html = '<h1>Your Playlists</h1>'
    for playlist in playlists:
        playlist_html += f"<p><strong>{playlist['name']}</strong></p>"
        playlist_html += f"<p><a href='/play/{playlist['uri']}'>Play</a></p>"

    return playlist_html

@app.route('/play/<playlist_uri>')
def play_playlist(playlist_uri):
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/')

    headers = {'Authorization': f'Bearer {access_token}'}
    play_data = {'context_uri': playlist_uri}
    response = requests.put(f"{API_BASE_URL}/me/player/play", headers=headers, json=play_data)

    if response.status_code == 204:
        return '<p>Playing playlist!</p><a href="/playlists">Back to Playlists</a>'
    else:
        return '<p>Error starting playback. Ensure you have an active device.</p>'

if __name__ == '__main__':
    app.run(debug=True)
