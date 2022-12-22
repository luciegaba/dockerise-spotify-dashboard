import pandas as pd
"""  """
from sqlalchemy import create_engine
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from mysql.connector import Error
#from credentials import CREDS_MYSQL_RAP,SQL_REQUEST_TRACKS,SQL_REQUEST_ARTISTS

import os
CREDS_MYSQL_RAP_USERNAME=os.environ.get("CREDS_MYSQL_RAP_USERNAME")
CREDS_MYSQL_RAP_PASSWORD=os.environ.get("CREDS_MYSQL_RAP_PASSWORD")
CREDS_MYSQL_RAP_HOST=os.environ.get("CREDS_MYSQL_RAP_HOST")
CREDS_MYSQL_RAP_DB=os.environ.get("CREDS_MYSQL_RAP_DB")
SQL_REQUEST_TRACKS=os.environ.get("SQL_REQUEST_TRACKS")
SQL_REQUEST_ARTISTS=os.environ.get("SQL_REQUEST_ARTISTS")

CREDS_MYSQL={"host":CREDS_MYSQL_RAP_HOST,
"database": CREDS_MYSQL_RAP_DB,
"username":CREDS_MYSQL_RAP_USERNAME,
"password":CREDS_MYSQL_RAP_PASSWORD}



def read_mysql_table(config,sql_request):
    """ Returns a pd.DataFrame with requested data from MySql
    Arguments:
    - config: dict of config parameters
    - sql_request: request SQL to get data
    """
    engine = create_engine(
        f"mysql+pymysql://{config.get('username')}:{config.get('password')}@{config.get('host')}/{config.get('database')}"
    )
    df = pd.read_sql_query(sql_request, engine)
    print(df)
    return df


def test_connection_mysql(config):
    try:
        connection = mysql.connector.connect(host=config.get('host'),
                                            database=config.get('database'),
                                            user=config.get('user'),
                                            password=config.get('password'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL")



if os.environ.get("CSV_OPTION")=="YES":
    tracks=pd.read_csv("components/data/tracks.csv")
    artists=pd.read_csv("components/data/artists.csv")
else: 
    tracks=read_mysql_table(CREDS_MYSQL,SQL_REQUEST_TRACKS)
    artists=read_mysql_table(CREDS_MYSQL,SQL_REQUEST_ARTISTS)
    
artists_list=list(set(artists["artist_name"].values.tolist()))
artists_list.sort()
artists_list=artists_list



       
