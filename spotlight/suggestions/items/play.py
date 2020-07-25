from spotlight.manager.manager import PlaybackManager
from spotlight.suggestions.items.item import Item


# Item classes that are used in more than one file should be written into this file

class SongItem(Item):
    def __init__(self, name: str, artists: str, image_name: str, id_: str):
        """
        Song Item Class
        :param name: Name of the song
        :param artists: Artists associated with the song
        :param image_name: This is the ALBUM ID of a song, use "" if the song is not cached
        :param id_: id/uri/term for song
        """
        Item.__init__(self, name, f"By {artists}", image_name if len(image_name) == 22 else "play",
                      PlaybackManager.play_song, "", id_, "exe")


class QueueItem(Item):
    def __init__(self, name: str, artists: str, image_name: str, id_: str):
        """
        Queue Item Class
        :param name: Name of the song
        :param artists: Artists associated with the song
        :param image_name: This is the ALBUM ID of a song, use "" if the song is not cached
        :param id_: id/uri/term for song
        """
        Item.__init__(self, name, f"By {artists}", image_name if len(image_name) == 22 else "list",
                      PlaybackManager.queue_song, "", id_, "exe")


class PlaylistItem(Item):
    def __init__(self, name: str, owner: str, image_name: str, id_: str):
        """
        Playlist Item Class
        :param name: Name of the playlist
        :param owner: owner associated with the playlist
        :param image_name: This is the PLAYLIST ID of a playlist, use "" if the song is not cached
        :param id_: id/uri for playlist
        """
        Item.__init__(self, name, f"By {owner}", image_name if len(image_name) == 22 else "playlist",
                      PlaybackManager.play_playlist, "", id_, "exe")


class ArtistItem(Item):
    def __init__(self, name: str, genre: str, image_name: str, id_: str):
        """
        Artist Item Class
        :param name: Name of the artist
        :param genre: artists main genre
        :param image_name: This is the ARTIST ID, use "" if the song is not cached
        :param id_: id/uri for artist
        """
        Item.__init__(self, name, genre, image_name if len(image_name) == 22 else "artist",
                      PlaybackManager.play_artist, "", id_, "exe")


class AlbumItem(Item):
    def __init__(self, name: str, artists: str, image_name: str, id_: str):
        """
        Album Item Class
        :param name: Name of the album
        :param artists: artists associated with album
        :param image_name: This is the ALBUM ID, use "" if the song is not cached
        :param id_: id/uri for album
        """
        Item.__init__(self, name, f"By {artists}", image_name if len(image_name) == 22 else "album",
                      PlaybackManager.play_album, "", id_, "exe")
