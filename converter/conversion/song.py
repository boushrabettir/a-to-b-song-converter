from dataclasses import dataclass
from typing import List
from db import update_links_in_db, query_song, add_song_row_in_db

@dataclass
class SongObject:
    """Struct holding data for a full song object"""

    song_name: str
    youtube_link: str | None
    spotify_link: str | None

@dataclass
class SongList:
    """Struct holding list of type SongObject"""

    list_of_songs: List[SongObject]

@dataclass
class Convert:
    song_list: SongList

    def create_playlist(self, **kwargs: dict) -> str:
        """"""

        playlist_title: str = kwargs.get("playlist_name")

        if kwargs.get("spotify"):
            """
            if the playlist already exists,
            ask if the user wants to rewrite the entire playlist
            if so do it
            if not prompt them again for a playlist name
            """
            pass
        elif kwargs.get("youtube"):
            pass
    
    def does_playlist_exist(title: str, youtube: bool, spotify: bool) -> bool:
        if youtube:
            pass
        if spotify:
            pass

    def add_song_to_playlist() -> str:
        pass

    def spotify_to_youtube(self, cli_args: any) -> str:
        """
        TODO
        After authentication of spotify and youtube,
        and asking for the name of the youtube playlist
        default will be the spotifys


        default will be set to a private playlist

        Loop through each song,
        query through db first
        if row is None find link through Youtube
        insert into DB
        """

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