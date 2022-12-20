from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import dash_table
import dash_daq as daq
from components.retrieving_sql import artists_list


# Several components for this page: search bar, gauge bar, dropdowns
# Differents under-parts:
    # artist_caracteristics_and_top 
    # statistics (radar graph)

search_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Input(id="input-artist",
                      type="search",
                      placeholder="Search for artist",
                      list='list-suggested-inputs',
                      autoComplete=True)),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

gauge_bar = daq.Gauge(
    showCurrentValue=True,
    id="popularity-artist",
    label='Popularity score',
    max=100,
    min=0,
)

dropdown_bar_songs = html.Div([
    dcc.Dropdown(id="dropdown-titles",
                 multi=True,
                 placeholder="Select song(s)"),
])
dropdown_bar_artist = html.Div([
    dcc.Dropdown(id="dropdown-artist",
                 multi=True,
                 placeholder="Select artist(s) to compare",
                 options=artists_list),
])

artist_caracteristics_and_top = dbc.Container([
    html.H4("Artist Overview", className='text-center'),
    dbc.Row([
        dbc.Col([
            html.H4("Which Artist would you search?",
                    id='chosen-artist',
                    className='text-center'),
            dbc.Row(gauge_bar),
            html.H6("Followers",
                    id='followers-artist',
                    className='text-center'),
        ]),

        dbc.Col([
            dbc.Row(html.H6("Most popular songs", className='text-center')),
            dash_table.DataTable(id='artist_songs',
                                 style_data={
                                     'fontSize': 14,
                                     'fontWeight': 'bold',
                                     'textAlign': 'center',
                                     'backgroundColor': '#f2f2f2',
                                     'border': '1px solid #d6d6d6'
                                 },
                                 style_header={
                                     'fontSize': 16,
                                     'fontWeight': 'bold',
                                     'textAlign': 'center',
                                     'backgroundColor': '#f2f2f2',
                                     'border': '1px solid #d6d6d6'
                                 },
                                 virtualization=True)
        ]),
        dbc.Col([
            dbc.Row(html.H6("Most popular albums", className='text-center')),
            dash_table.DataTable(id='artist_albums',
                                 fixed_rows={'headers': True},
                                 style_data={
                                     'fontSize': 14,
                                     'fontWeight': 'bold',
                                     'textAlign': 'center',
                                     'backgroundColor': '#f2f2f2',
                                     'border': '1px solid #d6d6d6'
                                 },
                                 style_header={
                                     'fontSize': 16,
                                     'fontWeight': 'bold',
                                     'textAlign': 'center',
                                     'backgroundColor': '#f2f2f2',
                                     'border': '1px solid #d6d6d6'
                                 })
        ])
    ])
])
statistics = dbc.Container([
    dbc.Row([
        html.Br(),
        html.H4("Analyzing Audio Features", className='text-center'),
        html.H6("Let's see how this artist is...", className='text-center')
    ]),
    dbc.Row([
        html.Br(),
        # artist panel
        dbc.Col([
            html.Br(),
            html.H6("Select an artist to compare with",
                    className='text-center'), dropdown_bar_artist,
            dcc.Graph(id='graph_spider_artist')
        ]),
        dbc.Col([
            html.Br(),
            html.H6("Select a song", className='text-center'),
            dropdown_bar_songs,
            dcc.Graph(id='graph_spider_songs')
        ])
    ])
])


layout_dashboard = html.Div(children=[
    html.Br(),
    html.Datalist(id='list-suggested-inputs',
                  children=[html.Option(value=word) for word in artists_list]),
    search_bar, artist_caracteristics_and_top, statistics
])
