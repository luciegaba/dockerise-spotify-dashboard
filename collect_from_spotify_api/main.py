import os
import pandas as pd

from scripts.collect_artists_name import get_rappers_exhaustive_list
from connection import (
    get_access_token,
    push_table_to_mysql,
    test_connection_mysql,
)
from scripts.scraping_api import (
    get_albums_from_artist,
    get_artist_caracteristics,
    get_spotify_artists_id,
    get_tracks_from_album,
)

CREDS_MYSQL = {
    "host": os.environ.get("CREDS_MYSQL_RAP_HOST"),
    "database": os.environ.get("CREDS_MYSQL_RAP_DB"),
    "username": os.environ.get("CREDS_MYSQL_RAP_USERNAME"),
    "password": os.environ.get("CREDS_MYSQL_RAP_PASSWORD"),
}

"""     # Get the list of artists and the access token
    if os.environ.get("CSV_OPTION")=="YES":
        tracks=pd.read_csv("data/tracks.csv")
        artists=pd.read_csv("data/artists.csv").drop(columns="index")
        print(tracks)
        push_table_to_mysql(CREDS_MYSQL, artists,"All artists","artists")
        push_table_to_mysql(CREDS_MYSQL, tracks, "All artists", "tracks")       

    else:  """
def main():

    list_artists = get_rappers_exhaustive_list(["rap francais"])
    # Get the Spotify IDs of the artists
    sp = get_access_token()
    dico_id = get_spotify_artists_id(list_artists, sp)
    print(dico_id)
    # For each artist, retrieve album and track data
    for artist, artist_id in dico_id.items():
        print(artist)
        # Refresh the token before each call to the Spotify API
        sp = get_access_token()
        albums = get_albums_from_artist(artist_id, sp)
        artist_feature = get_artist_caracteristics(artist_id, sp)
        artist_data = pd.DataFrame(data=artist_feature, index=[0])
        test_connection_mysql(CREDS_MYSQL)
        push_table_to_mysql(CREDS_MYSQL, artist_data, artist, "artists")
        data_tracks = pd.DataFrame(get_tracks_from_album(albums, sp))
        test_connection_mysql(CREDS_MYSQL)
        push_table_to_mysql(CREDS_MYSQL, data_tracks, artist, "tracks")


if __name__ == "__main__":
    main()
