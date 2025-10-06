from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from backend.core.db import Base

# ==========================================================
# Tabelle di associazione
# ==========================================================
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

# ==========================================================
# Modelli principali
# ==========================================================


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )
