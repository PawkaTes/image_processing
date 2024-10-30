from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Image
from app.schemas import ImageCreate, ImageResponse
from app.auth import get_current_user, create_access_token
from app.image_processing import process_image
from app.tasks import send_message
import os, shutil

app = FastAPI()

@app.post("/upload/", response_model=ImageResponse)
async def upload_image(
    title: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    user_id: str = Depends(get_current_user)
):
    filename = f"{title}_{file.filename}"
    file_path = f"images/{filename}"
    os.makedirs("images", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    metadata = process_image(file_path)
    image_record = Image(
        title=title,
        file_path=file_path,
        resolution=metadata["resolution"],
        size=metadata["size"],
    )
    
    db.add(image_record)
    db.commit()
    db.refresh(image_record)
    send_message("image_events", f"Image uploaded: {image_record.id}")
    
    return image_record
