
import dash_bootstrap_components as dbc
from dash import html


# Create Navigation Bar with logo, and several tabs


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        html.Img(
                            src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/2048px"
                            "-Spotify_logo_without_text.svg.png",
                            style={'height':'10%', 'width':'10%'},
                            id='photo-artist',
                            className='img-fluid'
                        ),
                        dbc.Col(html.A("GitHub", href="https://github.com/luciegaba", style={"color": "white"}))
                    ],
                    align="center",
                    className="g-0",
                )
            ),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Home", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Artist dashboard", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/dashboard_artist",
                style={"textDecoration": "none"},
            ),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Recommandations", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/recommandation_system",
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="dark",
    dark=True,
)