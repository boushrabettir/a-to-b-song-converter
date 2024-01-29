from dataclasses import dataclass
import os
from typing import Set, List
from conversion.song import SongObject

@dataclass
class ErrorSong:
    """"""
    
    error_song: SongObject

@dataclass
class ErrorSongList:
    """"""

    error_list: List[ErrorSong]


@dataclass
class Error:
    """"""

    def verify_env_variables() -> None:
        """"""

        REQUIRED_VARS: Set[str] = set(["YT",
                                       ])
        for env_variable in REQUIRED_VARS:
            if env_variable not in os.environ:
                raise EnvironmentError(f"{env_variable} has not been set. Please try again!\n")
              
    def table_no_exist(table_name: str) -> str:
        """"""

        return f"{table_name} does not exist."

    def link_no_exist(type: bool, song: SongObject) -> str:
        """"""

        platform: str  = "Youtube" if type else "Spotify"
        return f"{platform} link does not exist for {song.song_name} ({song.artist_name})\n"
    
    def amount_of_deleted_songs() -> str:
        return f""
