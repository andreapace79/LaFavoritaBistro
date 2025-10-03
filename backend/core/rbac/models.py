from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from core.db import Base

# Associazione utenti-ruoli
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True, nullable=False),
)

# Associazione ruoli-permessi
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True, nullable=False),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True, nullable=False),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    roles = relationship("Role", secondary=user_roles, back_populates="users")

    # Relazione con audit log tramite stringa completa
    logs = relationship("modules.audit.models.AuditLog", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )
