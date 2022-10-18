from pydantic import BaseModel
from typing import Optional


class ResultSchema(BaseModel):
    file_name: Optional[str]
    transcription: Optional[str]

