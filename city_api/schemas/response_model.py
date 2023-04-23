from .base import Base


class ResponseModel(Base):
    status: str
    message: str
