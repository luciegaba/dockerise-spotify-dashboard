import os
from pylast import LastFMNetwork, Tag

def get_rappers_exhaustive_list(tag_names: list) -> list:
    """Retrieves the exhaustive list of rappers corresponding to the given tag.
    Parameters:
    - tag_name: the name of the tag to use for the search (example: "rap fr")

    Returns:
    - a list of artist names corresponding to the tag
    """
    # Retrieve environment variables
    api_key = os.environ["LASTFM_API_KEY"]
    api_secret = os.environ["LASTFM_API_SECRET"]
    # Create an instance of LastFMNetwork
    lastfm = LastFMNetwork(api_key=api_key, api_secret=api_secret)

    #Create an instance to stock names
    artists_name=[]
    # Iterate on tags
    for tag_name in tag_names:
    # Create a Tag object
        tag = Tag(tag_name, lastfm)

        # Retrieve the list of artists corresponding to the tag
        results = tag.get_top_artists(limit=1000)

        # Extract the names of the artists from the results list
        names = [top_item.item.get_name() for top_item in results]
        print(f"Artists concerning {tag_name} tag are",len(names))
        artists_name+=names
    return list(set(artists_name))
