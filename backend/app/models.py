from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

# Load the base class for declarative class definitions
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    audios = relationship("Audio", back_populates="owner")
    playlists = relationship("Playlist", back_populates="owner")

# Audio Model
class Audio(Base):
    __tablename__ = "audios"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    cloud_path = Column(String, nullable=False)
    transcoded = Column(Boolean, default=False, nullable=False)
    metadata = Column(JSON, nullable=True)
    waveform = Column(JSON, nullable=True)
    duration = Column(Integer, nullable=True)
    sample_rate = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    owner = relationship("User", back_populates="audios")
    playlist_id = Column(Integer, ForeignKey("playlists.id"), nullable=True)

# Playlist Model
class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    owner = relationship("User", back_populates="playlists")
    audios = relationship("Audio", back_populates="playlist_id")
