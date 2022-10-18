from db import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID,BYTEA
from uuid import uuid4


class ResultModel(Base):
    __tablename__ = "results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    transcription = Column(String)
    file = Column(String, nullable=False)
    image = Column(BYTEA, nullable=False)
