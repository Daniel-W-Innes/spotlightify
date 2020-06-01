import os
from os import sep, path, mkdir
from queue import Queue
from threading import Thread
from time import sleep

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon
from pynput.mouse import Button, Controller
from spotipy import Spotify, oauth2, SpotifyException

from caching import CachingThread, SongCachingThread, ImageCachingThread, ImageQueue
from config import USERNAME, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from definitions import ASSETS_DIR, CACHE_DIR
from interactions import Interactions
from shortcuts import listener
from ui import Ui

#  Allow users to use the default spotipy env variables


scope = "streaming user-library-read user-modify-playback-state user-read-playback-state user-library-modify " \
        "playlist-read-private playlist-read-private"


class Spotlightify:
    def __init__(self):
        self.app = QApplication([])
        self.queue = Queue()
        self.sp_oauth = self.get_sp_oauth()
        self.token_info = self.sp_oauth.get_cached_token()
        self.authenticated_spotify = self.get_authenticated_spotify(self.token_info["access_token"])
        self.interactions = Interactions(self.authenticated_spotify, self.token_info, self.sp_oauth, self.exit_app,
                                         self.queue)
        self.ui = Ui(self.interactions)
        self.tray = self.get_tray()
        self.app = QApplication([])
        self.setup_app()

    @staticmethod
    def get_sp_oauth():
        return oauth2.SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID') if os.getenv('SPOTIPY_CLIENT_ID') else CLIENT_ID,
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET') if os.getenv(
                'SPOTIPY_CLIENT_SECRET') else CLIENT_SECRET,
            redirect_uri=REDIRECT_URI, scope=scope,
            username=os.getenv('USERNAME') if os.getenv('USERNAME') else USERNAME)

    @staticmethod
    def get_authenticated_spotify(token):
        try:
            return Spotify(auth=token)
        except SpotifyException:
            print("User token could not be created")
            raise

    def exit_app(self):
        self.ui.close()  # visually removes ui quicker
        raise Exception("Exit Command")

    def show_ui(self):
        if not self.ui.isActiveWindow() or self.ui.isHidden():
            self.ui.show()
        sleep(0.1)
        self.interactions.refresh_token()
        self.ui.raise_()
        self.ui.activateWindow()
        self.focus_ui()
        self.ui.function_row.refresh()  # refreshes function row buttons

    def focus_ui(self):  # Only way I could think of to properly focus the ui
        mouse = Controller()
        # mouse position before focus
        mouse_pos_before = mouse.position
        # changing the mouse position for click
        target_pos_x = self.ui.pos().x() + self.ui.textbox.pos().x()
        target_pos_y = self.ui.pos().y() + self.ui.textbox.pos().y()
        mouse.position = (target_pos_x, target_pos_y)
        mouse.click(Button.left)
        mouse.position = mouse_pos_before

    def tray_icon_activated(self, reason):
        if reason == self.tray.Trigger:  # tray.Trigger is left click
            self.show_ui()

    @staticmethod
    def create_cache():
        if not path.exists(CACHE_DIR):
            mkdir(CACHE_DIR)

    def start_cashing(self):
        image_queue = ImageQueue()

        self.create_cache()

        song_caching_thread = SongCachingThread(self.queue, image_queue)
        song_caching_thread.start()

        image_caching_thread = ImageCachingThread(image_queue)
        image_caching_thread.start()

        playlist_caching_thread = CachingThread(self.authenticated_spotify, "playlists", self.queue, image_queue)
        playlist_caching_thread.start()

        liked_caching_thread = CachingThread(self.authenticated_spotify, "liked", self.queue, image_queue)
        liked_caching_thread.start()

    @staticmethod
    def get_tray():
        icon = QIcon(f"{ASSETS_DIR}img{sep}logo_small.png")
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        tray.setToolTip("Spotlightify")
        return tray

    def get_menu(self):
        menu = QMenu()
        open_ui = QAction("Open")
        open_ui.triggered.connect(self.show_ui)
        menu.addAction(open_ui)

        exit_ = QAction("Exit")
        exit_.triggered.connect(self.exit_app)
        menu.addAction(exit_)
        return menu

    @staticmethod
    def start_listener(open_ui):
        listener_thread = Thread(target=listener, daemon=True, args=(open_ui,))
        listener_thread.start()

    def add_menu_the_tray(self, menu):
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.tray_icon_activated)

    def setup_app(self):
        self.app.setQuitOnLastWindowClosed(False)
        menu = self.get_menu()
        self.start_listener(menu)
        self.start_cashing()
        self.add_menu_the_tray(menu)

    def start_app(self):
        self.app.exec_()


if __name__ == '__main__':
    app = Spotlightify()
    app.start_app()
