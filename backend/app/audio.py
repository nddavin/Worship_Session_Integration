from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .models import Base, User

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
