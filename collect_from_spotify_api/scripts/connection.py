import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import os
import spotipy
import requests


def get_access_token(refresh_token=None):
    """
    Get access token from Spotify API using client id and secret.
    """
    client_id = os.environ['SPOTIPY_CLIENT_ID']
    print(client_id)
    client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
    print(client_secret)
    oauth_url = "https://accounts.spotify.com/api/token"
    data = {"client_id": client_id, "client_secret": client_secret}
    if refresh_token:
        # If a refresh token is provided, use it to get a new access token
        data["grant_type"] = "refresh_token"
        data["refresh_token"] = refresh_token
    else:
        # Otherwise, use the client id and secret to get an access token
        data["grant_type"] = "client_credentials"
    response = requests.post(oauth_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        sp = spotipy.Spotify(auth=token_data["access_token"])
        print(sp)
        return sp
    else:
        print(f"Error requesting access token: {response.status_code}")
        return None



def test_connection_mysql(config):
    """
    Test connection to MySQL database using provided configuration.
    """
    try:
        connection = mysql.connector.connect(
            host=config.get('host'),
            database=config.get('database'),
            user=config.get('username'),
            password=config.get('password')
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)

def push_table_to_mysql(config, df, artist, table):
    """
    Push provided dataframe to MySQL database using provided configuration.
    """
    engine = create_engine(
        f"mysql+pymysql://{config.get('username')}:{config.get('password')}@{config.get('host')}/{config.get('database')}"
    )
    df.to_sql(con=engine.connect(), name=table, if_exists='append')
    print(f"{artist} data successfully imported in mysqldb")
