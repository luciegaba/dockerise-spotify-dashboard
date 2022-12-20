import os
import pandas as pd

from collect_artists_name import get_rappers_exhaustive_list
from connection import (
    get_access_token,
    push_table_to_mysql,
    test_connection_mysql,
)
from scraping_api import (
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


def main():
    # Get the list of artists and the access token
    list_artists = get_rappers_exhaustive_list(["rap fr","french rap", "rap francais"])
    sp = get_access_token()

    # Get the Spotify IDs of the artists
    dico_id = get_spotify_artists_id(list_artists, sp)

    # For each artist, retrieve album and track data
    for artist, artist_id in dico_id.items():
        while True:
            try:
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
                break  # If everything went well, exit the loop
            except Exception as e:  # Handle all errors
                print(f"An error occurred: {e}")
                # If the token has expired, refresh it and retry the request
                if "The access token expired" in str(e):
                    sp = get_access_token(refresh_token=sp["refresh_token"])
                    continue
                # Otherwise, exit the loop and move on to the next artist
                break
            # print(f'problem with this artist:{artist}')


if __name__ == "__main__":
    main()
