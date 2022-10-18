from http import HTTPStatus
from typing import List
import validators
from fastapi import HTTPException, APIRouter, UploadFile, Depends
from services import lm
from crud import add_url_result, add_file_result, get_images
from db import SessionLocal
from models import ResultSchema as ReSchema, ResultModel as ReModel
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post('/ocr_detection/image/')
async def detect_url_image(image_url: str, db: Session = Depends(get_db)) -> ReSchema:
    if validators.url(image_url):
        if image_url.endswith(('.png', '.jpg', '.jpeg')):
            result = ReSchema()
            result.file_name = image_url
            result.transcription = lm.predict_from_url(image_url)
            add_url_result(db, result)
            return result
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=f"You must enter an url of an image"
    )


@router.post('/ocr_detection/file/')
async def detect_file_image(file: UploadFile, db: Session = Depends(get_db)) -> ReSchema:
    if file.filename.endswith(('.png', '.jpg', '.jpeg')):
        result = ReSchema()
        result.file_name = file.filename
        result.transcription = lm.predict_from_file(file)
        add_file_result(db, result, file)
        return result
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=f"You must enter an url of an image"
    )


@router.get('/ocr_detection/')
async def detected_images(db: Session = Depends(get_db)) -> List[ReModel]:
    images = List[ReModel]
    images = get_images(db)
    return images
