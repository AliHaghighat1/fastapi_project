import uuid
from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    public_id = Column(
        String(36),
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )

    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(20))
    email = Column(String(255), unique=True)
    balance = Column(Float)
    is_active = Column(Boolean)