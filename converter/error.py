from dataclasses import dataclass
import os
from typing import Set, List
from conversion.song import SongObject

@dataclass
class ErrorSong:
    """"""
    
    error_song: str

@dataclass
class ErrorSongList:
    """"""

    error_list: List[ErrorSong]


@dataclass
class Error:
    """"""

    def verify_env_variables() -> None:
        """"""

        REQUIRED_VARS: Set[str] = set(["YT"])

        for env_variable in REQUIRED_VARS:
            if env_variable not in os.environ:
                raise EnvironmentError(f"{env_variable} has not been set. Please try again!\n")
              
    def table_no_exist(table_name: str) -> str:
        """"""

        return f"{table_name} does not exist."

    def song_does_not_exist(type: bool, song: SongObject) -> str:
        """"""

        platform: str  = "Youtube" if type else "Spotify"
        return f"{platform} link does not exist for {song.song_name} ({song.artist_name})\n"
    
    def empty_item_response() -> str:
        """Response after request execution is empty."""

        return "Reponse has empty items."

    def channelId_does_not_exist(username: str) -> str:
        """Response after request execution does not exist."""

        return f"Channel ID for '{username}' does not exist."
    
    def auth_token_does_not_exist() -> str:
        """Authentication credentials token does not exist."""

        return "Authentication token does not exist, please try again."    
    
    def not_found_song(song_name: str) -> str:
        """Song not found after query"""

        return f"'{song_name}' is not found."
    
    def no_playlists() -> str:
        """No playlists exist."""

        return f"No playlists found."
    
    def amount_of_deleted_songs() -> str:
        return f""
