from sklearn.decomposition import PCA
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from components.kmeans_recommandation import prepare_data_for_kmeans
from components.retrieving_sql import tracks,artists
list_var_to_desc = [
        "track_name", "danceability", "energy", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence"
    ]



def cluster_pca_graph(choice, obs_song, obs_artist):
    """
    Returns graph of PCA 2 components to have a visual overview of positions of artist/songs calling the function "graph_for_indiv_update"
    Arguments:
        - choice: 
        - obs_song: song selected (if users want songs )
        - obs_artist: artist selected 

    """
    if choice == "Artist":
        choice = 'artist'
        obs = obs_artist
    elif choice == "Song":
        obs = obs_song
        choice = 'track_name'
    try:
        X_normalise, df_for_pred = prepare_data_for_kmeans(choice, tracks)
        index_obs = df_for_pred[df_for_pred[choice] == obs].index.tolist()[0]
        cluster = df_for_pred["cluster"].loc[index_obs]
        fig = graph_for_indiv_update(X_normalise, obs, cluster, choice,
                                    df_for_pred)
        stats = pd.DataFrame(
            df_for_pred.groupby(df_for_pred["cluster"]).median().loc[cluster].
            reset_index()).to_dict(orient='records')
        cluster = f"{obs} belongs to Cluster {cluster}"
    except:
        cluster = f"Cluster"
        fig = go.Figure()
        stats = pd.DataFrame().to_dict(orient='records')
    return cluster, fig, stats



def graph_for_indiv_update(X_normalise: np.array,obs:str,cluster_obs:int,target:str,df:pd.DataFrame):
    """
    Returns graph of PCA 2 components to have a visual overview of positions of artist/songs. 
    Arguments:
        - X_normalize:  X scaled 
        - obs: particular information given by user (a song or an artist...)
        - cluster_obs: cluster of our "obs"
        - target: "artist" or "song" depending on wished informations
        - df: "tracks" dataframe
    """
    acp = PCA(n_components=2)
    acp.fit(X_normalise) 
    df_graph=pd.concat([pd.DataFrame(acp.transform(X_normalise)),df["cluster"],df[target]],axis=1)
    df_graph_cluster=df_graph[df_graph["cluster"]==cluster_obs]
    coord_obs=df_graph[[0,1]][df_graph[target]==obs].values.tolist()[0]
    fig = px.scatter(df_graph_cluster, x=0, y=1,text=target,color_discrete_sequence=['rgb(94, 201, 98,0.5)'])
    fig.add_trace(go.Scatter(x=[coord_obs[0]], y=[coord_obs[1]], mode = 'markers+text', marker_symbol = 'pentagon',marker_size = 25,marker_color=["rgb(231, 63, 116)"],text=obs))
    fig.update_traces(textposition="bottom center")
    fig.update_layout(showlegend=False,autosize = True,hovermode='closest')
    return fig



def graph_spider_for_one_artist(artist_input: str , list_songs_selected: list ):
    """
    Returns Radar graph comparing mean Audio Features from an artist with one of its song(s)
    Arguments:
        - artist_input: artist name
        - list_songs_selected: list of selected songs by users
    """
    list_var_to_desc = [
        "track_name", "danceability", "energy", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence"
    ]

    audio_features = tracks[list_var_to_desc][tracks['artist'].str.contains(
        artist_input)]
    list_var_to_desc.remove("track_name")
    audio_features_mean = audio_features.drop(columns="track_name").mean()
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(r=audio_features_mean.values,
                        theta=list_var_to_desc,
                        fill='toself',
                        name='Mean Audio Features'))
    try:
        for song in list_songs_selected:
            print(song)
            audio_features_song = audio_features[audio_features["track_name"]
                                                == song].values.tolist()
            print(audio_features_song)
            fig.add_trace(
                go.Scatterpolar(r=audio_features_song[0],
                                theta=list_var_to_desc,
                                fill='toself',
                                name=f'{song} Audio Features'))
            print(fig)

            fig.update_layout(polar=dict(radialaxis=dict(visible=True, )),
                            showlegend=False)

        return fig
    except:
        return fig



def graph_spider_for_comparaison_artists(artist_input:str, artists_selected:list):
    """
    Returns Radar graph comparing mean Audio Features from an artist with another one
    Arguments:
        - artist_input: artist name
        - artists_selected: list of selected artists by users to compare with
    """
    list_var_to_desc = [
        "track_name", "danceability", "energy", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence"
    ]

    audio_features = tracks[list_var_to_desc][tracks['artist'].str.contains(
        artist_input)]
    list_var_to_desc.remove("track_name")
    audio_features_mean = audio_features.drop(
        columns="track_name").mean().values
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(r=audio_features_mean,
                        theta=list_var_to_desc,
                        fill='toself',
                        name='Mean Audio Features'))
    try:
        for artist_compare in artists_selected:
            print(artist_compare)
            list_var_to_desc = [
                "track_name", "danceability", "energy", "speechiness",
                "acousticness", "instrumentalness", "liveness", "valence"
            ]
            audio_features = tracks[list_var_to_desc][
                tracks['artist'].str.contains(artist_compare)]
            list_var_to_desc.remove("track_name")
            audio_features_mean = audio_features.drop(
                columns="track_name").mean().values
            fig.add_trace(
                go.Scatterpolar(r=audio_features_mean,
                                theta=list_var_to_desc,
                                fill='toself',
                                name=f'{artist_compare} Mean Audio Features'))

            fig.update_layout(polar=dict(radialaxis=dict(visible=True, )),
                              showlegend=False)

        return fig
    except:
        return fig



def get_selected_obs_from_graph(selectData:dict, choice:str):
    """
    Returns list with suggestions depending on the graph PCA. Typically, if the user zooms around its song, and select area around, we can retrieve observations near this point. 
    Arguments:
    - selectData: Part selected of points in graph_pca
    - choice: "Song" or "Artist"
    """
    filtList = []
    if choice == "Artist":
        choice = 'artist'
    elif choice == "Song":
        choice = 'track_name'
    try:
        data = selectData["points"]
        for i in range(len(data) - 1):
            filtList.append(data[i]["text"])
        return filtList
    except:
        return filtList






