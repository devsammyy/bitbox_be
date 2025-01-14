from enum import Enum
from ..db.database import Base
from ..department.department_model import Department
from sqlalchemy import Column, String, ForeignKey, text, Enum as SQLAlchemyEnum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UserRole(Enum):
    ADMIN = "admin"
    MEMBER = "member"
    HOD = "hod"


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, server_default=text("gen_random_uuid()"), nullable=False)
    first_name = Column(String(length=50), index=True, nullable=True)
    last_name = Column(String(length=50), index=True, nullable=True)
    username = Column(String(length=50), unique=True,
                      index=True, nullable=False)
    gender = Column(String(length=50), index=True, nullable=True)
    phone_number = Column(String(length=50), index=True, nullable=True)
    email = Column(String(length=50), unique=True, index=True)
    full_name = Column(String(length=100), nullable=True)
    password = Column(String, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey(
        "departments.id", ondelete="CASCADE"), nullable=True)
    department = relationship("Department", back_populates="users")
    role = Column(
        SQLAlchemyEnum(UserRole, name="userrole"),
        nullable=False
    )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True,
                        server_onupdate=text("now()"))
