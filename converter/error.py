from dataclasses import dataclass
import os
from typing import Set

@dataclass
class Error:
    """"""

    def verify_env_variables() -> None:
        """"""

        REQUIRED_VARS: Set[str] = set([])
        for env_variable in os.environ:
            if env_variable not in REQUIRED_VARS:
                raise EnvironmentError("")
    
    def table_no_exist(table_name: str) -> str:
        """"""

        return f"{table_name} does not exist."

    def link_no_exist(type: bool, song_name: str, artist: str) -> str:
        """"""

        platform: str  = "Youtube" if type else "Spotify"
        return f"{platform} link does not exist for {song_name} ({artist})\n"
    
    def amount_of_deleted_songs() -> str:
        return f""
