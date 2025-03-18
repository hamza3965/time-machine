import config
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID_SPOTIFY = config.CLIENT_ID_SPOTIFY
CLIENT_SECRET_SPOTIFY = config.CLIENT_SECRET_SPOTIFY
SPOTIFY_DISPLAY_NAME = config.SPOTIFY_DISPLAY_NAME
URL_REDIRECT = "http://example.com"


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url = "https://www.billboard.com/charts/hot-100" + date
response = requests.get(url=url, headers=header)

soup = BeautifulSoup(response.text, "html.parser")
song_names = soup.select("li h3, li .o-chart-results-list-row-container")
top_100_songs = song_names[:100]

song_titles = [song.getText().strip() for song in top_100_songs]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID_SPOTIFY,
        client_secret=CLIENT_SECRET_SPOTIFY,
        cache_path="token.txt",
        redirect_uri=URL_REDIRECT,
        scope="playlist-modify-private",
        username=SPOTIFY_DISPLAY_NAME,
    )
)

user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
