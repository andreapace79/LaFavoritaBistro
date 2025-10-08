import sys
import os

# Aggiungo il percorso backend al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.core.db import SessionLocal, Base, engine
from backend.core.rbac.models import Role, Permission, role_permissions, user_roles
from backend.modules.users.models import User
from backend.modules.areas import crud as areas_crud, schemas as areas_schemas
from backend.modules.tables import crud as tables_crud, schemas as tables_schemas
from backend.modules.tables.models import Table
from backend.modules.orders.models import Order
from backend.modules.orders import crud as orders_crud, schemas as orders_schemas
from passlib.hash import bcrypt


def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # === Ruoli ===
        admin_role = db.query(Role).filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin")
            db.add(admin_role)
            db.commit()

        staff_role = db.query(Role).filter_by(name="staff").first()
        if not staff_role:
            staff_role = Role(name="staff")
            db.add(staff_role)
            db.commit()

        # === Permessi ===
        permissions = [
            ("users.read",   "Leggere utenti"),
            ("users.write",  "Creare/modificare utenti"),
            ("areas.manage", "Gestire aree e tavoli"),
            ("orders.manage","Gestire comande"),           # ✅ aggiunto
        ]
        for code, desc in permissions:
            if not db.query(Permission).filter_by(code=code).first():
                db.add(Permission(code=code, description=desc))
        db.commit()

        # === Associa tutti i permessi al ruolo admin ===
        db_perms = db.query(Permission).all()
        for p in db_perms:
            exists = db.execute(
                role_permissions.select().where(
                    (role_permissions.c.role_id == admin_role.id)
                    & (role_permissions.c.permission_id == p.id)
                )
            ).fetchone()
            if not exists:
                db.execute(
                    role_permissions.insert().values(
                        role_id=admin_role.id, permission_id=p.id
                    )
                )
        db.commit()

        # === Utente admin ===
        admin_user = db.query(User).filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                password_hash=bcrypt.hash("admin123"),
                is_active=True,
            )
            db.add(admin_user)
            db.commit()

        # === Associa admin_user al ruolo admin ===
        exists = db.execute(
            user_roles.select().where(
                (user_roles.c.user_id == admin_user.id)
                & (user_roles.c.role_id == admin_role.id)
            )
        ).fetchone()
        if not exists:
            db.execute(
                user_roles.insert().values(
                    user_id=admin_user.id, role_id=admin_role.id
                )
            )
            db.commit()

        # === Area demo "Interno" ===
        area = areas_crud.get_area_by_name(db, "Interno")
        if not area:
            area = areas_crud.create_area(
                db,
                areas_schemas.AreaCreate(
                    name="Interno",
                    layout_meta={"note": "Area principale interna"},
                ),
            )

        # === Tavoli demo ===
        existing_tables = tables_crud.list_tables_by_area(db, area.id)
        if not existing_tables:
            tables_crud.create_table(
                db, tables_schemas.TableCreate(area_id=area.id, name="T1", seats=4)
            )
            tables_crud.create_table(
                db, tables_schemas.TableCreate(area_id=area.id, name="T2", seats=2)
            )
        db.commit()

        # === Ordini (comande) demo ===
        has_orders = db.query(Order).first() is not None
        if not has_orders:
            # Tavolo T1 → comanda aperta
            t1 = db.query(Table).filter_by(name="T1").first()
            if t1:
                order1 = orders_schemas.OrderCreate(
                    table_id=t1.id,
                    items=[
                        orders_schemas.OrderItemCreate(name="Spritz", quantity=2, price=5.0),
                        orders_schemas.OrderItemCreate(name="Tagliere misto", quantity=1, price=12.0),
                    ],
                )
                orders_crud.create_order(db, order1)

            # Tavolo T2 → comanda chiusa
            t2 = db.query(Table).filter_by(name="T2").first()
            if t2:
                order2 = orders_schemas.OrderCreate(
                    table_id=t2.id,
                    items=[
                        orders_schemas.OrderItemCreate(name="Caffè", quantity=2, price=1.2),
                        orders_schemas.OrderItemCreate(name="Acqua naturale", quantity=1, price=1.5),
                    ],
                )
                created = orders_crud.create_order(db, order2)
                orders_crud.close_order(db, created.id)

        # === Output finale ===
        print("✅ Seed completato:")
        print(f"   • Utente admin → admin / admin123")
        print(f"   • Ruolo admin con {len(db_perms)} permessi")
        print(f"   • Area creata: {area.name}")
        print(f"   • Tavoli demo: T1, T2")
        if not has_orders:
            print("   • Comande demo create per T1 e T2")
        else:
            print("   • Comande già presenti: nessuna nuova creata")

    except Exception as e:
        db.rollback()
        print(f"❌ Errore durante il seed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
