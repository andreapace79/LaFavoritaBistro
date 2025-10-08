from logging.config import fileConfig
import sys
import pathlib

from sqlalchemy import engine_from_config, pool
from alembic import context

# ========= Path & Base =========
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from backend.core.db import Base
from backend.core.config import settings

# ⚠️ Importa i modelli nell'ordine giusto:
# 1) RBAC & USERS (dipendenze base)
from backend.core.rbac import models as rbac_models
from backend.modules.users import models as users_models

# 2) Il resto dei moduli che possono riferirsi a users/rbac
from backend.modules.audit import models as audit_models
from backend.modules.areas import models as areas_models
from backend.modules.tables import models as tables_models
from backend.modules.suppliers import models as suppliers_models
from backend.modules.inventory import models as inventory_models

# ========= Alembic config =========
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata,
        literal_binds=True, dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.", poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
