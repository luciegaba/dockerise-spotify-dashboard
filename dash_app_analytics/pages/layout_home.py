from dash import html

layout_home = html.Div([
    html.H1('Welcome to our Dash web app!', style={'text-align': 'center', 'color': '#1DB954', 'margin': '20px 0'}),
    html.P('This project was created to help music fans, particularly French rap fans, understand their affinity for music using data science. Our app includes a MySQL database and a Dash web application that provides an overview of artists and recommendations based on a machine learning model.', style={'text-align': 'center', 'color': '#6c757d', 'margin': '20px 0'}),
    html.H2('Audio Features from Spotify', style={'text-align': 'center', 'color': '#1DB954', 'margin': '20px 0'}),
    html.H5('To understand our model and statistics, you must be briefed on used criterion: ', style={'text-align': 'center', 'color': '#6c757d', 'margin': '20px 0'}),

    html.Div([
        html.P(
            '''
            Danceability: This variable reflects how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A track with a high danceability score will be more energetic and more likely to get people moving.
            ''',
            style={'font-weight': 'bold'}
        ),
        html.P(
            '''
            Energy: This variable reflects the intensity and activity of a track. It ranges from 0 (least energetic) to 1 (most energetic). A track with a high energy score will typically be fast, loud, and have strong percussion.
            ''',
            style={'font-weight': 'bold'}
        ),
        html.P(
            '''
            Speechiness: This variable detects the presence of spoken words in a track. It ranges from 0 (least speech-like) to 1 (most speech-like). A track with a high speechiness score will typically have a lot of spoken word content, such as a podcast or a news report.
            ''',
            style={'font-weight': 'bold'}
        ),
        html.P(
            '''
            Acousticness: This variable reflects the presence of acoustic instruments in a track. It ranges from 0 (least acoustic) to 1 (most acoustic). A track with a high acousticness score will typically have a lot of acoustic instruments, such as guitar or piano.
            ''',
            style={'font-weight': 'bold'}
        ),
        html.P(
            '''
            Instrumentalness: This variable reflects the presence of instrumental music in a track. It ranges from 0 (least instrumental) to 1 (most instrumental). A track with a high instrumentalness score will typically have very little or no vocal content, such as an instrumental version of a song.
            ''',
            style={'font-weight': 'bold'}
        ),
        html.P(
            '''
            Liveness: This variable reflects the presence of a live audience in a track. It ranges from 0 (least live) to 1 (most live). A track with a high liveness score will typically have a lot of audience noise and a live feel to it.
            ''',
            style={'font-weight': 'bold'}
        ),
        html.P(
            '''
            Valence: This variable reflects the overall positivity or negativity of a track. It ranges from 0 (least positive) to 1 (most positive). A track with a high valence score will typically be more upbeat and happy, while a track with a low valence score will be more sad or melancholy.
            ''',
            style={'font-weight': 'bold'}
        ),
    ], style={'padding': '20px'})
], style={'background-color': '#f8f9fa', 'padding': '30px', 'text-align': 'center'})


