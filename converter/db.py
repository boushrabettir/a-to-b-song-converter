import psycopg2
import os
from typing import Tuple
from conversion.song import SongObject

TABLE_NAME: str = os.getenv("TABLE_NAME")

def instantiate_connection():
    """Instantiates database connection."""

    uri: str = os.getenv("DB_URI")
    return psycopg2.connect(uri)

def create() -> None:
    """Creates table in database."""

    with instantiate_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS
            {TABLE_NAME}(song TEXT, artist TEXT, spotify_id TEXT[], youtube_id TEXT[], type TEXT[])"""
        )

        connection.commit()

def is_link_same(current_db_link: str, new_link: str) -> bool:
    """Determines if current link is the same as the new link."""

    return current_db_link == new_link

def update_links_in_db(current_song_object: SongObject) -> None:
    """Inserts song into row; Updates link values."""

    SONG_NAME: str = current_song_object.song_name
    ARTIST_NAME: str = current_song_object.artist_name
    IDENTIFIER: str = current_song_object.identifier

    with instantiate_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT *
            FROM {TABLE_NAME} WHERE
            song = %(song)s""",
            {"song": SONG_NAME}
        )

        row = cursor.fetchone()
        if row:
            song_output, artist_output, id_output, type_output = row

            if not is_link_same(id_output, IDENTIFIER):
                cursor.execute(
                    f"UPDATE {TABLE_NAME} SET id = %s WHERE song = %s",
                    (IDENTIFIER, SONG_NAME)
                )

        connection.commit()

def add_song_row_in_db(current_song_object: SongObject) -> None:
    """"""

    SONG_NAME: str = current_song_object.song_name
    ARTIST_NAME: str = current_song_object.artist_name
    IDENTIFIER: str = current_song_object.identifier

    # with instantiate_connection() as connection:
    #     cursor = connection.cursor()
    #     cursor.execute(
    #                 f"""INSERT INTO {TABLE_NAME} (song, artist, id, type)
    #                 VALUES (%s, %s, %s, %s)""",
    #                 (
    #                     SONG_NAME,
    #                     YOUTUBE_LINK,
    #                     SPOTIFY_LINK
    #                 )
    #             )
        
    #     connection.commit()
       
def query_song(**kwargs: dict) -> Tuple[str, str, str] | None:
    """Returns the row for the given song; returns None if the song does not exist."""

    SONG_NAME: str | None = kwargs.get("song")

    with instantiate_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
                    f"""SELECT *
                    FROM {TABLE_NAME} WHERE
                    SONG_NAME = %(song_name)s""",
                    {"song_name": SONG_NAME}
                )

        row = cursor.fetchone()
        
        return row if row else None
            
def delete_song(song_name: str, artist_name: str) -> None:
    """"""
    pass
