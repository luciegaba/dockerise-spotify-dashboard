import os
import pandas as pd

from scripts.collect_artists_name import get_rappers_exhaustive_list
from scripts.connection import (
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

import os
import pandas as pd

def main():

#If csv option : not requesting
    if os.environ.get("CSV_OPTION")=="YES":
        tracks = pd.read_csv("data/tracks.csv").drop(columns="index")
        artists = pd.read_csv("data/artists.csv").drop(columns="index")
        print(tracks)
        push_table_to_mysql(CREDS_MYSQL, artists,"All artists","artists")
        push_table_to_mysql(CREDS_MYSQL, tracks, "All artists", "tracks")     


#Requesting spotify
    else: 
        list_artists = get_rappers_exhaustive_list(["rap fr", "rap francais"])
        print("List artists from Lastfm:",list_artists)
        sp = get_access_token()
        dico_id_ = get_spotify_artists_id(list_artists, sp)
        for artist, artist_id in dico_id_.items():
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
