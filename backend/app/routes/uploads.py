from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AudioFile, User
from ..auth import get_current_user
from ..tasks import transcode_and_extract_task
import uuid

router = APIRouter()

@router.post("/presign")
def presign_upload(
    filename: str = Form(...),
    content_type: str = Form(...),
    current_user: User = Depends(get_current_user)
) -> dict:
    key = f"uploads/{current_user.id}/{uuid.uuid4()}_{filename}"
    upload_url = f"https://example-bucket.s3.amazonaws.com/{key}"  
    return {"upload_url": upload_url, "method": "PUT", "headers": {"Content-Type": content_type}, "key": key}

@router.post("/complete")
def complete_upload(
    key: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    audio = AudioFile(owner_id=current_user.id, filename=key.split("/")[-1], cloud_path=key)
    db.add(audio)
    db.commit()
    db.refresh(audio)
    transcode_and_extract_task.delay(audio.id, key)
    return {"ok": True, "audio_id": audio.id}
