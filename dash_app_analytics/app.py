

import pandas as pd
import dash
from dash import html

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from components.graphs import  cluster_pca_graph,graph_spider_for_one_artist,graph_spider_for_comparaison_artists,get_selected_obs_from_graph

from components.retrieving_sql import tracks,artists

from pages.header import navbar
from pages.layout_dashboard import layout_dashboard
from pages.layout_home import layout_home
from pages.layout_recommander import layout_recommander

import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output

import pandas as pd



# Boostrap theme for App
# All are available at : https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/

bootstrap_theme = [dbc.themes.CYBORG]
# Define App from Dash
app = dash.Dash(__name__, external_stylesheets=bootstrap_theme)
app.config.suppress_callback_exceptions = True
server = app.server

# layout rendu par l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=True), navbar,
    html.Div(id='page-content')
])




""" 
GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/luciegaba",
) """



# callback pour mettre à jour les pages


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home' or pathname == '/':
        return layout_home
    elif pathname == '/dashboard_artist':
        return layout_dashboard
    elif pathname == '/recommandation_system':
        return layout_recommander


@app.callback(Output('chosen-artist', "children"),
              Input('input-artist', 'value'),
              prevent_initial_call=True)
def display_artist(artist_input):
    return artist_input


@app.callback(Output('artist_songs', "data"),
              Input('input-artist', 'value'),
              prevent_initial_call=True)
def display_songs(artist_input):
    spotify_songs = tracks[["track_name", "album"
                            ]][tracks['artist'].str.contains(artist_input)]
    return spotify_songs.head(20).to_dict(orient='records')


@app.callback(Output('artist_albums', "data"),
              Input('input-artist', 'value'),
              prevent_initial_call=True)
def display_albums(artist_input):
    spotify_albums = pd.DataFrame(
        tracks["album"][tracks['artist'].str.contains(artist_input)].unique())
    return spotify_albums.head(20).to_dict(orient='records')


@app.callback(Output('popularity-artist', "value"),
              Input('input-artist', 'value'),
              prevent_initial_call=True)
def display_popularity(artist_input):
    popularity = artists["artist_popularity"][artists['artist_name'] ==
                                              artist_input].values.tolist()[0]
    return int(popularity)


@app.callback(Output('followers-artist', "children"),
              Input('input-artist', 'value'),
              prevent_initial_call=True)
def display_followers(artist_input):
    followers = artists["followers"][artists['artist_name'] ==
                                     artist_input].values.tolist()[0]
    return f"{followers} Followers"


@app.callback(Output('dropdown-titles', "options"),
              Input('input-artist', 'value'),
              prevent_initial_call=True)
def get_songs_list(artist_input):
    songs = tracks["track_name"][tracks['artist'] ==
                                 artist_input].values.tolist()
    return songs


@app.callback(Output('graph_spider_songs', 'figure'),
              Input('input-artist', 'value'),
              Input('dropdown-titles', 'value'),
              prevent_initial_call=True)
def update_graph_spider_song(artist_input, list_songs_selected):
    fig=graph_spider_for_one_artist(artist_input,list_songs_selected)
    return fig


@app.callback(Output('graph_spider_artist', 'figure'),
              Input('input-artist', 'value'),
              Input('dropdown-artist', 'value'),
              prevent_initial_call=True)
def update_graph_spider_artist(artist_input, artists_selected):
    fig=graph_spider_for_comparaison_artists(artist_input,artists_selected)
    return fig


@app.callback(Output('selected_artist', 'disabled'),
              Output('selected_songs', 'disabled'),
              Input('radio_choice', 'value'),
              prevent_initial_call=True)
def get_choices_options(choice):
    if choice == "Artist":
        return (False, True)
    else:
        return (False, False)


@app.callback(Output('selected_songs', "options"),
              Input('selected_artist', 'value'),
              prevent_initial_call=True)
def get_songs_list(artist_input):
    if artist_input == None:
        songs = tracks["track_name"].values.tolist()
    else:
        songs = tracks["track_name"][tracks['artist'] == artist_input].values.tolist()
    return songs


@app.callback(Output('cluster', 'children'),
              Output('pca_graph', 'figure'),
              Output('stats', 'data'),
              Input('radio_choice', 'value'),
              Input('selected_songs', 'value'),
              Input('selected_artist', 'value'),
              prevent_initial_call=True)
def update_cluster_for_ind(choice, obs_song, obs_artist):
    cluster, fig, stats=cluster_pca_graph(choice, obs_song, obs_artist)
    return cluster, fig, stats


@app.callback(Output('selection_from_graph', 'children'),
              Input('pca_graph', 'selectedData'),
              Input("radio_choice", "value"),
              prevent_initial_call=True)
def selectData(selectData, choice):
    filtList=get_selected_obs_from_graph(selectData, choice)
    return  html.Ul([html.Li(x) for x in filtList])
    


if __name__ == '__main__':
    app.run_server(debug=True)
