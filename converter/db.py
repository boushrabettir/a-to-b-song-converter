import psycopg2
import os
from conversion.song import SongObject, SongList
from typing import Tuple

TABLE_NAME: str = os.getenv("TABLE_NAME")

def instantiate_connection():
    """Instantiates database connection."""

    uri: str = os.getenv("DB_URI")
    return psycopg2.connect(uri)

def create() -> None:
    pass

def is_link_same(current_db_link: str, new_link: str) -> bool:
    """Determines if current link is the same as the new link."""

    return current_db_link == new_link

def update_links_in_db(current_song_object: SongObject) -> None:
    """Inserts song into row; Updates link values."""

    SONG_NAME: str = current_song_object.song_name
    YOUTUBE_LINK: str = current_song_object.youtube_link
    SPOTIFY_LINK: str = current_song_object.spotify_link

    with instantiate_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT *
            FROM {TABLE_NAME} WHERE
            SONG_NAME = %(song_name)s""",
            {"song_name": SONG_NAME}
        )

        row = cursor.fetchone()
        if row:
            song_key, youtube_value, spotify_value = row

            if youtube_value or not is_link_same(youtube_value, YOUTUBE_LINK):
                cursor.execute(
                    f"UPDATE {TABLE_NAME} SET youtube = ?",
                    (youtube_value, song_key)
                )

            if spotify_value or not is_link_same(spotify_value, SPOTIFY_LINK):
                cursor.execute(
                    f"UPDATE {TABLE_NAME} set spotify = ?",
                    (spotify_value, song_key)
                )

        connection.commit()

def add_song_row_in_db(current_song_object: SongObject) -> None:
    """"""

    SONG_NAME: str = current_song_object.song_name
    YOUTUBE_LINK: str = current_song_object.youtube_link
    SPOTIFY_LINK: str = current_song_object.spotify_link

    with instantiate_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
                    f"""INSERT INTO {TABLE_NAME} (song, youtube, spotify)
                    VALUES (%s, %s, %s)""",
                    (
                        SONG_NAME,
                        YOUTUBE_LINK,
                        SPOTIFY_LINK
                    )
                )
        
        connection.commit()
        
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
            

