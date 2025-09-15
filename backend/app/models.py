from sqlalchemy.ext.declarative import declarative_base

# Load the base class for declarative class definitions
Base = declarative_base()

# Import Audio and Playlist models
from .audio import Audio
from .playlist import Playlist
