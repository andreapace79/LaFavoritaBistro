import sys
import os

# Aggiungo il percorso backend al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.db import SessionLocal, Base, engine
from core.rbac.models import User, Role, Permission, UserRole, RolePermission
from passlib.hash import bcrypt

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Ruoli
        admin_role = Role(name="admin")
        staff_role = Role(name="staff")

        db.add_all([admin_role, staff_role])
        db.commit()

        # Permessi di esempio
        perms = [
            Permission(code="users.read", description="Leggere utenti"),
            Permission(code="users.write", description="Creare/modificare utenti"),
            Permission(code="areas.manage", description="Gestire aree e tavoli"),
        ]
        db.add_all(perms)
        db.commit()

        # Associa permessi ad admin
        for perm in perms:
            db.add(RolePermission(role_id=admin_role.id, permission_id=perm.id))

        db.commit()

        # Utente admin
        admin_user = User(
            username="admin",
            password_hash=bcrypt.hash("admin123"),
            is_active=True
        )
        db.add(admin_user)
        db.commit()

        # Associa admin_user al ruolo admin
        db.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))
        db.commit()

        print("✅ Seed completato: utente admin creato con password 'admin123'")
    except Exception as e:
        db.rollback()
        print(f"❌ Errore durante il seed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
