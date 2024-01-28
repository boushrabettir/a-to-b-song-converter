from typing import dataclass, List
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build

@dataclass
class PlaylistObject:
    """Attributes that define a playlist object"""
    
    name: str
    description: str | None
    playlist_id: str

@dataclass
class PlaylistList:
    """A custom list holding a custom class, PlaylistObject"""

    playlist: List[PlaylistObject]

@dataclass
class Youtube:
    """A Youtube class interacting with Youtube API"""

    def instantiate_youtube() -> any:
        YT_KEY: str = os.getenv("YT")
        YOUTUBE_OBJ = build("youtube",
                            "v3",
                                youtube_obj=YT_KEY)
        
        return YOUTUBE_OBJ
        
    def retrieve_channel_id(self, username: str) -> str:
        """Retrieves channel id to retrieve playlists"""

        rq = self.instantiate_youtube().search().list(part="id",
                                       type="channel",
                                       q=username)
        res=rq.execute()

        return res['items'][0]['id']['channelId']
        
    def retrieve_playlists(self, username: str) -> PlaylistList:
        """Retrieves all users playlist in a custom PlaylistObject class"""

        user_playlists = PlaylistList()

        channel_id: str = self.retrieve_channel_id(username)

        rq = self.instantiate_youtube().playlists().list(
            part="snippet",
            channelId=channel_id,
        )
        res = rq.execute()

        for response_object in res["items"]:
            
            playlist_name: str = response_object["snippet"]["title"]
            playlist_desc: str = response_object["snippet"]["description"]
            playlist_id: str = response_object["id"]
            
            current_object = PlaylistObject(
                name=playlist_name,
                description=playlist_desc,
                playlist_id=playlist_id,
            )

            user_playlists.playlist.append(current_object)

        return user_playlists
    
    def find_playlist(self, username: str, playlist_input_name: str) -> PlaylistObject | None:
        """Finds a specific playlist within the PlaylistList custom object"""

        all_user_playlists: PlaylistList = self.retrieve_playlists(username)
        found_playlist: PlaylistObject | None = [current_playlist for current_playlist in all_user_playlists if current_playlist["name"].lower() == playlist_input_name.lower()]

        return found_playlist

    def create_youtube_playlist():
        pass

    def delete_youtube_playlist():
        pass
    
    def add_song(playlist_name: str, song_name: str):
        pass

@dataclass
class Spotify:
    """A Spotify class interacting with Spotipy"""
    

    def instantiate_spotify() -> spotipy.Spotify:
        """Instantiates connection to Spotify"""

        CLIENT_ID: str = os.getenv("SPOTIFY_ID")
        CLIENT_SECRET: str = os.getenv("SPOTIFY_SECRET")

        return spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET
            )
        )
    
    def retrieve_playlists(self) -> PlaylistList:
        """Retrieves all users playlist in a custom PlaylistObject class"""

        user_playlists = PlaylistList()

        spotify_instance = self.instantiate_spotify()
        
        users_playlists = spotify_instance.current_user_playlists()

        for playlist in users_playlists["items"]:
            playlist_name: str = playlist["name"]
            playlist_description: str = playlist["description"]
            playlist_id: str = playlist["id"]
    
            current_object = PlaylistObject(
                name=playlist_name,
                description=playlist_description,
                playlist_id=playlist_id
            )

            user_playlists.playlist.append(current_object)
        
        return user_playlists


    # TODO - Appropriates DRY
    def find_playlist(self, playlist_input_name) -> PlaylistObject:
        """Finds a specific playlist within the PlaylistList custom object"""

        all_user_playlists: PlaylistList = self.retrieve_playlists()
        found_playlist: PlaylistObject | None = [current_playlist for current_playlist in all_user_playlists if current_playlist["name"].lower() == playlist_input_name.lower()]

        return found_playlist
        

    def create_spotify_playlist(self, playlist_name_input: str, playlist_desc_input: str | None) -> None:
        """Creates a new Spotfiy playlist for the user"""

        spotify_instance = self.instantiate_spotify()
        current_user = spotify_instance.me()["id"]

        spotify_instance.user_playlist_create(
            current_user,
            name=playlist_name_input,
            public=False,
            description=(playlist_desc_input if playlist_desc_input else "new playlist")
        )

    def delete_spotify_playlist():
        pass

    def add_song(playlist_name: str, song_name: str):
        pass

        


        