from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True)
    hashed_password = Column(String(256))
    role = Column(String(50), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    audios = relationship("AudioFile", back_populates="owner")
    playlists = relationship("Playlist", back_populates="owner")

class AudioFile(Base):
    __tablename__ = "audio_files"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(256))
    cloud_path = Column(String(512))
    transcoded = Column(Boolean, default=False)
    metadata = Column(JSON, default={})
    waveform = Column(JSON, default=[])
    duration = Column(Integer, default=0)
    sample_rate = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="audios")
    playlist_id = Column(Integer, ForeignKey("playlists.id"))

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)
    audios = relationship("AudioFile", backref="playlist")
    owner = relationship("User", back_populates="playlists")
