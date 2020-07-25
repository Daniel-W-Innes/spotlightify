import json
from datetime import datetime
from os import sep

from definitions import CACHE_DIR


class CacheHolder:
    """Holds cached data
    """
    playlist_cache = {"length": 0, "playlists": {}}
    song_cache = {"length": 0, "songs": {}}
    artist_cache = {"length": 0, "artist": {}}
    album_cache = {"length": 0, "playlists": {}}
    last_refresh = datetime.now()

    @staticmethod
    def check_reload(_type: str):  # will refresh every 5 minutes (300 seconds)
        """Reloads cached items if time since last reload has surpassed 5 minutes

        Args:
            _type (str): Either song, playlist, artist, album or all
        """
        time_passed = (datetime.now() - CacheHolder.last_refresh).total_seconds()
        if time_passed > 150:
            CacheHolder.last_refresh = datetime.now()
            CacheHolder.reload_holder(_type)

    @staticmethod
    def reload_holder(_type: str):
        '''
        Reloads data to static variables inside of this class, use the check_reload method if you want the cache to refresh only once every 5 mins
        :param _type: Either song, playlist, artist, album or all
        :return:
        '''

        # load cached songs
        def load_cach(path: str, cache_name: str):
            try:
                with open(path, 'r') as f:
                    return dict(sorted(json.load(f)[cache_name].items(), key=lambda x: x[1]['name']))
            except FileNotFoundError:
                return

        if _type == "song" or _type == "all":
            CacheHolder.song_cache = load_cach(song_cache_file_path, "songs")
        if _type == "artist" or _type == "all":
            CacheHolder.artist_cache = load_cach(artist_cache_file_path, "artists")
        if _type == "album" or _type == "all":
            CacheHolder.album_cache = load_cach(album_cache_file_path, "albums")
        if _type == "playlist" or _type == "all":
            CacheHolder.playlist_cache = load_cach(playlist_cache_file_path, "playlists")
        if _type == "liked" or _type == "all":
            CacheHolder.liked_cache = load_cach(liked_cache_file_path, "songs")


# Cached file paths
song_cache_file_path = f"{CACHE_DIR}songs.json"
playlist_cache_file_path = f"{CACHE_DIR}playlists.json"
album_cache_file_path = f"{CACHE_DIR}albums.json"
artist_cache_file_path = f"{CACHE_DIR}artists.json"
liked_cache_file_path = f"{CACHE_DIR}liked.json"
album_art_path = f"{CACHE_DIR}art{sep}"
