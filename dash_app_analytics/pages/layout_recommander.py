
from dash import html,dcc, dash_table
import dash_bootstrap_components as dbc


from components.retrieving_sql import artists_list

radio_bar = dbc.Row(
    [
        dbc.Col(dcc.RadioItems(options=['Artist', 'Song'], id="radio_choice"))])
   


dropbar_songs = dcc.Dropdown(id="selected_songs",
                             placeholder="Select songs",
                             value="")

dropbar_artist = dcc.Dropdown(id="selected_artist",
                              placeholder="Select Artist",
                              options=artists_list,
                              value="")



graph_cluster = dcc.Graph(id='pca_graph')



select_options_part = dbc.Container([
   html.H4('Spotify recommandations system', style={'textAlign': 'center'}),
    dbc.Row([html.Br(),
         dbc.Col(html.H6("What recommandations you need?")),
        dbc.Col([radio_bar,]),
        dbc.Col([dropbar_artist]),
        dbc.Col([dropbar_songs])])])

clustering_part= dbc.Container([
    dbc.Row([
      dbc.Col([
        html.Br(),
        html.Br(),
        html.H4("Clustering approach recommandation", className='text-center'),
        html.H6("Our algorithm intents to make a basic recommandation from our music taste with artist/song selection. Contrary to complex Spotify recommandations system algorithm, which requires a large amount of knowledges/data from users, our recommandation are made with a basic well-known algorithm: K-Means", className='text-center'),
        html.Br()]),
      dbc.Col([html.Br(),
      dbc.Row([html.H6("Please Select on Graph an area around the marker (pentagon) with the following tools:"),
      html.Img(src='assets/selection.png', alt='image')]),
      html.Br(),
      html.Br(),
      dbc.Row(
      graph_cluster),
      html.Br(),
      html.H6("Clustering", id='cluster', className='text-center'),
      ])])])
table_reports_part= dbc.Container([dbc.Row([
         html.Br(),
         html.H6("From the previous graph, we recommend you the several artists/songs:", className='text-center'),
         dbc.Alert("", color="info", id='selection_from_graph')])])

layout_recommander=html.Div(children=[
    html.Br(),
    select_options_part,
    clustering_part,
    table_reports_part])

