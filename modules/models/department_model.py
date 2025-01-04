from sqlalchemy import Column, String, ForeignKey, text, Enum as SQLAlchemyEnum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from modules.db.database import Base
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = "departments"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, server_default=text("gen_random_uuid()"), nullable=False)
    name = Column(String(length=50), index=True, nullable=True)
    users = relationship("User", back_populates="department")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True,
                        server_onupdate=text("now()"))
