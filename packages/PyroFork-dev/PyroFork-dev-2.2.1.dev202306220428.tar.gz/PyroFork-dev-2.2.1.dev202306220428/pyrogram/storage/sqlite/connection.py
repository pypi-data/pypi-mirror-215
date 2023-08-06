from .cursor import AsyncCursor
from pyrogram.utils import run_sync
from sqlite3 import Connection
from threading import Thread

class AsyncConnection(Thread):
    def __init__(self, connection: Connection):
        self.connection = connection
        self.started = False