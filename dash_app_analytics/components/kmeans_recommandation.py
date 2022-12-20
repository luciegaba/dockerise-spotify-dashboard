
from sklearn.preprocessing import StandardScaler # Import du module de sklearn qu'on va utiliser pour normaliser les données
from sklearn.cluster import KMeans






def prepare_data_for_kmeans(target,df):
    """ 
    Returns scale data + clusters for df by doing kmeans clustering depending on the target (artist or song clustering). Features selected for kmeans are mentioned above. 
    Arguments:
    - target : 'artist' or 'song' depending on user's choice
    - df: tracks" dataframe
    """

    features=['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

    df_groupby=df.copy()
    df_groupby["artist"]=df_groupby["artist"].apply(lambda x: x.split(",")[0]) # To get only main artists for a track
    df_groupby_=df_groupby.copy()

    if target =="artist":
        k=9
    elif target=="track_name":
        k=8

    df_groupby_= df_groupby_[features].groupby(df_groupby_[target]).median().reset_index()
    X = df_groupby_[features].values
    sc = StandardScaler()
    X_normalise = sc.fit_transform(X)
    km = KMeans(n_clusters=k,random_state=0)
    preds=km.fit_predict(X_normalise)
    df_for_graph=df_groupby_.copy()
    df_for_graph['cluster'] = preds
    return X_normalise,df_for_graph


