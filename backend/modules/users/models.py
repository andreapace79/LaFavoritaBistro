# backend/modules/users/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.db import Base
from backend.core.rbac.models import user_roles  # usa la tabella di rbac

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1)

    roles = relationship(
        "backend.core.rbac.models.Role",
        secondary=user_roles,
        back_populates="users",
        lazy="joined"
    )
