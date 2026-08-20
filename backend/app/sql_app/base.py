from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.sql_app.models import (
    User,
    Candidate,
    Resume,
    Interview,
    Message,
    Report,
)