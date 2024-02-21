import argparse
from conversion.song import Convert, SongList
from conversion.playlist import PlaylistList, PlaylistObject, Youtube, Spotify
from dotenv import load_dotenv

load_dotenv()

def extract_user_value():
    """"""
    print_welcome_message() 

    parser = argparse.ArgumentParser(
        description=""
    )

    parser.add_argument(
        "--yt",
        action="store_true",
        help="Youtube to Spotify"
    )

    parser.add_argument(
        "--sp",
        action="store_true",
        help="Spotify to Youtube"
    )

    parser.add_argument(
        "--help",
        action="store_true"
    )

    return parser.parse_args()


def print_welcome_message() -> str:
    return """
        Please type --1 for YT->SP
        or --2 for SP->YT
    """



def main():
    """Entry point of program."""

    # user_choice = extract_user_value()

    # if user_choice.help:
    #     print_welcome_message()

    # elif user_choice.sp:
    #     playlist_title: str = input("Playlist title please")
    #     playlist_desc: str | None = input("Playlist desc pls")

    # temp = Youtube()
    # found = temp.query_song("Starships")
    # playlist = temp.find_playlist("bbgodd3ss", "Lethal Company")

    # print(found)
    # print("\n")
    # print(playlist)
    
    # temp.add_song(playlist[0].playlist_id, found.list_of_songs[0].identifier)

    temp = Spotify()
    
    print(temp.query_song("Starships"))

    


if __name__ == '__main__':
    main()