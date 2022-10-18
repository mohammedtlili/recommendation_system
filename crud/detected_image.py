import requests
from fastapi import UploadFile
from models import ResultSchema as ReSchema, ResultModel as ReModel
from sqlalchemy.orm import Session
from PIL import Image


def add_url_result(db: Session, result: ReSchema):
    blob = Image.open(requests.get(result.file_name, stream=True).raw).tobytes(encoder_name="raw")
    db_result = ReModel(transcription=result.transcription, file=result.file_name, image=blob)
    db.add(db_result)
    db.commit()
    return db_result.id


def add_file_result(db: Session, result: ReSchema, file: UploadFile):
    blob = Image.open(file.file).tobytes(encoder_name="raw")
    db_result = ReModel(transcription=result.transcription, file=result.file_name, image=blob)
    db.add(db_result)
    db.commit()
    return db_result.id


def get_images(db: Session):
    return db.query(ReModel).all()
