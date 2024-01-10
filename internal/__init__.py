import os
from .store import Database, Metadata
from .store import logger

db = Database(os.getenv("STORE", "sqlite:///db.sqlite"))