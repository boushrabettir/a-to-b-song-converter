from dataclasses import dataclass
from typing import List
from db import update_links_in_db, query_song, add_song_row_in_db, delete_song
from error import Error
from typing import Tuple
import os


@dataclass
class SongObject:
    """Struct holding data for a full song object"""

    artist_name: str
    youtube_link: Tuple[str, str] | None
    spotify_link: Tuple[str, str] | None

@dataclass
class SongList:
    """Struct holding list of type SongObject"""

    list_of_songs: List[SongObject]

@dataclass
class Convert:
    song_list: SongList

    def spotify_to_youtube(self, cli_args: any) -> str:

        # check to see if the playlist already exists
        self.create_playlist()
        
        for song_object in self.song_list:
            if query_song(song=song_object.song_name):
                # update the link
                # add it to the playlist
                update_links_in_db(song_object)
            else:
                add_song_row_in_db(song_object)

            self.add_song_to_playlist()

        return 

    def youtube_to_spotify(self, cli_args: any) -> str:
        pass


