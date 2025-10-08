from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.core.db import Base
from backend.core.rbac.models import user_roles

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    roles = relationship(
        "backend.core.rbac.models.Role",
        secondary=user_roles,
        back_populates="users",
        lazy="joined",
    )
