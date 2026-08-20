from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so SQLAlchemy registers them
# with Base.metadata.
from app.sql_app.models.candidate import Candidate
from app.sql_app.models.interview import Interview
from app.sql_app.models.message import Message
from app.sql_app.models.report import Report
from app.sql_app.models.resume import Resume
from app.sql_app.models.user import User