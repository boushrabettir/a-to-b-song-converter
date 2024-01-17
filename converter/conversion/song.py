from dataclasses import dataclass
from typing import List
from db import update_links_in_db, query_song, add_song_row_in_db, delete_song
from error import Error
from typing import Tuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

CLIENT_ID = os.getenv("ID")
CLIENT_SECRET = os.getenv("SECRET")


@dataclass
class SongObject:
    """Struct holding data for a full song object"""

    artist_name: str
    youtube_link: Tuple(str, str) | None
    spotify_link: Tuple(str, str) | None

@dataclass
class SongList:
    """Struct holding list of type SongObject"""

    list_of_songs: List[SongObject]

@dataclass
class Convert:
    song_list: SongList

    def return_sp_instance(self) -> spotipy.Spotify:
        return spotipy.Spotify(
                auth_manager=SpotifyClientCredentials(
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET)
                    )
    
    def create_playlist(self, **kwargs: dict) -> str:
        """"""

        playlist_title: str = kwargs.get("playlist_name")
        playlist_description: str | None = kwargs.get("playlist_desc")
        
        if kwargs.get("spotify"):
            """
            if the playlist already exists,
            ask if the user wants to rewrite the entire playlist
            if so do it
            if not prompt them again for a playlist name
            """
            spotify_instance = self.return_sp_instance()
            current_user = spotify_instance.me()['id']
            found_playlist = self.does_playlist_exist(playlist_title, spotify=True)
            
            
            if found_playlist:
                pass
            
            else:
                spotify_instance.user_playlist_create(current_user,
                                                      name=playlist_title,
                                                      public=False, 
                                                      description=(playlist_description if playlist_description else "new playlist"))



        elif kwargs.get("youtube"):
            pass
    
   
    def does_playlist_exist(self, title: str, youtube: bool=False, spotify: bool=False) -> any:

        if youtube:
            found_yt_playlist = ""

            return found_yt_playlist
        if spotify:
            spotify_instance = self.return_sp_instance()
            found_sp_playlist = spotify_instance.search(q=title, type='playlist')

            return found_sp_playlist


        
            

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

    def delete_songs_in_playlist(self, playlist_link: str, amount: str | None):
        """"""
        if amount and int(amount) < 0:
            raise Error().amount_of_deleted_songs()

        default_amount: int = int(amount) if amount else 0

    


            