from typing import List, Tuple
from dataclasses import dataclass
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.oauth2.credentials import Credentials
from conversion.song import SongObject, SongList
from error import ErrorSong, ErrorSongList
from googleapiclient.discovery import build
from dotenv import load_dotenv
from error import Error

load_dotenv()

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

    def instantiate_youtube(self) -> any:
        """Instantiates Youtube object."""

        Error().verify_env_variables()

        YT_KEY: str = os.getenv("YT")
        YOUTUBE_OBJ = build("youtube",
                            "v3",
                            developerKey=YT_KEY)
        
        return YOUTUBE_OBJ
    
    def authentication() -> any:
        """Request authentication for manipulating playlists."""


    def retrieve_channel_id(self, username: str) -> str:
        """Retrieves channel id to retrieve playlists"""

        rq = self.instantiate_youtube().search().list(part="id",
                                       type="channel",
                                       q=username)
        res=rq.execute()
        
        if not res.get("items")[0].get("id").get("channelId"):
            raise Error().empty_item_response()
        
        return res.get("items")[0].get("id").get("channelId")

    def retrieve_playlists(self, username: str) -> PlaylistList:
        """Retrieves all users playlist in a custom PlaylistObject class"""

        user_playlists = PlaylistList([])

        channel_id: str = self.retrieve_channel_id(username)
 
        rq = self.instantiate_youtube().playlists().list(
            part="snippet",
            channelId=channel_id,
        )

        res = rq.execute()
        
        if not res.get("items"):
            raise Error().empty_item_response()
        
        for response_object in res.get("items"):
            
            playlist_name: str = response_object.get("snippet").get("title")
            playlist_desc: str = response_object.get("snippet").get("description")
            playlist_id: str = response_object.get("id")
            
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

        found_playlist : PlaylistList | None = []

        for current_playlist in all_user_playlists.playlist:
            if current_playlist.name.lower() == playlist_input_name.lower():
                found_playlist.append(current_playlist)


        return found_playlist

    def create_youtube_playlist(self, playlist_name_input: str, playlist_desc_input: str | None):
        """Creates Youtube playlist for designated user."""

    def delete_youtube_playlist(self, playlist_id: str):
        """Deletes Youtube playlist for designated user."""
    
    def query_song(self, song_name: str) -> Tuple[SongList, ErrorSongList]:
        """Query a music video song. Returns a list of song objects"""
       
        rq = self.instantiate_youtube().search().list(
            part="snippet",
            type="video",
            q=song_name,
            maxResults=5
        )
        res = rq.execute()

        # Add error song in error list for ending CLI message
        error_song_list = ErrorSongList([])
        if not res.get("items"):
            song_not_found = ErrorSong(song_name)
            error_song_list.list_of_songs.append(song_not_found)

        # TODO - IF res.get("items") IS GREATER THAN 1 THAN PROMPT THE USER TO FIGURE OUT WHICH SONG
        
        song_list = SongList([])

        for response_object in res.get("items"):
            object_name = response_object.get("snippet").get("title")
            object_artist = response_object.get("snippet").get("channelTitle")
            object_id = response_object.get("id").get("videoId")

            current_song_object = SongObject(object_name, object_artist, object_id)
            song_list.list_of_songs.append(current_song_object)

        return (song_list, error_song_list)
        
    def add_song(self, playlist_id: str, video_id: str) -> None:
        """Add's a specific song to a specific playlist."""

        rq = self.instantiate_youtube().playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )

        # Add authentication header to manipluate playlist
        authentication_credentials_token = self.authentication()
        rq.headers["Authorization"] = f"Bearer {authentication_credentials_token}"

        rq.execute()

@dataclass
class Spotify:
    """A Spotify class interacting with Spotipy"""
    

    def instantiate_spotify(self) -> spotipy.Spotify:
        """Instantiates connection to Spotify"""

        #Error().verify_env_variables()

        CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID")
        CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET
            )
        )
        return sp

    def retrieve_playlists(self) -> PlaylistList:
        """Retrieves all users playlist in a custom PlaylistObject class"""

        user_playlists = PlaylistList([])

        spotify_instance = self.instantiate_spotify()
        
        # users_playlists = spotify_instance.current_user_playlists()
        # print(user_playlists)
        # results = spotify_instance.search(q='weezer', limit=20)
        # for idx, track in enumerate(results['tracks']['items']):
        #     print(idx, track['name'])

        # for playlist in users_playlists.get("items"):
        #     playlist_name: str = playlist["name"]
        #     playlist_description: str = playlist["description"]
        #     playlist_id: str = playlist["id"]
    
        #     current_object = PlaylistObject(
        #         name=playlist_name,
        #         description=playlist_description,
        #         playlist_id=playlist_id
        #     )

        #     user_playlists.playlist.append(current_object)
        
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

    def delete_spotify_playlist(self, playlist: PlaylistObject) -> None:
        """"""

        spotify_instance = self.instantiate_spotify()

        spotify_instance.playlist_remove_all_occurrences_of_items(
            playlist_id=playlist.playlist_id
        )

        spotify_instance.playlist_change_details(
            playlist_id=playlist.playlist_id,
            name=f"[DELETED]{playlist.name}",
            public=False,
            collaborative=False,
            description=f"[DELETED]{playlist.description}"
        )
        
    def add_song(self, playlist: PlaylistObject, song_name: str) -> None:
        """"""

        found_song: SongObject | None = self.query_song(song_name)

        if not found_song:
            raise Error().song_does_not_exist()

        spotify_instance = self.instantiate_spotify()

        spotify_instance.playlist_add_items(playlist_id=playlist.playlist_id,
                                                           items=[found_song.identifier],
                                                           position=None)
 
    def query_song(self, song_name: str) -> SongObject | None:
            """"""
            rq = self.instantiate_spotify().search(q=song_name, type="track")
            
            if not rq.get("tracks").get("items"):
                return None

            found_songs = rq.get("tracks").get("items")

            if len(found_songs) == 1:
                current_song_obj = SongObject(
                song_name=found_songs[0].get("name"),
                artist_name=found_songs[0].get("artist"),
                identifier=found_songs[0].get("uri")
                )

                return current_song_obj
            

            # TODO - Ask which song it is!