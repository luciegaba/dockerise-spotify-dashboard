def get_spotify_artists_id(list_artists, sp):
    """
    Get the Spotify IDs of the artists.
    """
    print("Getting Artists from LastFM")
    dico_id = {}
    for artist in list_artists:
        results = sp.search(q=artist, type='artist')
        if results['artists']['total'] > 0:
            first_result = results['artists']['items'][0]
            artist_name = first_result['name']
            artist_id = first_result['id']
            dico_id[artist_name] = artist_id
        else:
            print(f"No results found for artist {artist}")
    return dico_id


def get_artist_caracteristics(artist_id, sp):
    """
    Returns a dictionary of artist characteristics.
    
    Parameters:
    - artist_id: Spotify ID of the artist
    - sp: authenticated Spotify API object
    """
    dict_artist = {}
    result_artist = sp.artist(artist_id)
    dict_artist["artist_id"] = artist_id
    dict_artist["artist_name"] = result_artist["name"]
    dict_artist["artist_popularity"] = result_artist["popularity"]
    dict_artist["genre"] = ", ".join(result_artist["genres"])
    dict_artist["followers"] = result_artist["followers"]["total"]
    return dict_artist


def get_albums_from_artist(artist_id, sp):
    """
    Returns a dictionary mapping album names to their Spotify IDs.
    
    Parameters:
    - artist_id: Spotify ID of the artist
    - sp: authenticated Spotify API object
    """
    albums_dic_id = {}
    result = sp.artist_albums(artist_id, album_type=["album","single"])
    for album in result["items"]:
        albums_dic_id[album["name"]] = album["id"]
    return albums_dic_id



def get_tracks_from_album(albums_dic_id, sp):
    """
    Returns a list of dictionaries containing track information.
    
    Parameters:
    - albums_dic_id: dictionary mapping album names to their Spotify IDs
    - sp: authenticated Spotify API object
    """
    list_tracks_for_artist = []
    for album, album_id in albums_dic_id.items():
        for track in sp.album_tracks(album_id)["items"]:
            tracks = {}
            tracks["track_id"] = track["id"]
            tracks["track_name"] = track["name"]
            tracks["album"] = album
            tracks["artist"] = ", ".join([artist["name"] for artist in track["artists"]])
            try:
                tracks.update(sp.audio_features(tracks["track_id"])[0])
            except: 
                pass
            track_info = sp.track(tracks["track_id"])
            tracks["popularity"] = track_info["popularity"]
            tracks["release_date"] = track_info["album"]["release_date"]
            list_tracks_for_artist.append(tracks)

    return list_tracks_for_artist

