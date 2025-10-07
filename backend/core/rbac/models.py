# backend/core/rbac/models.py
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.core.db import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True, nullable=False),
    extend_existing=True,
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True, nullable=False),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True, nullable=False),
    extend_existing=True,
)

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, default="")

    users = relationship("backend.modules.users.models.User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, default="")

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
