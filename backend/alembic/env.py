from logging.config import fileConfig
import sys
import pathlib

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ==========================================================
# Setup path per importare core e modules
# ==========================================================
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from core.db import Base
# Importiamo esplicitamente i modelli per assicurarci che Alembic li veda
from backend.modules.users import models as users_models
from backend.core.rbac import models as rbac_models
from backend.modules.audit import models as audit_models
from backend.modules.areas import models as areas_models
from backend.modules.tables import models as tables_models
from backend.modules.suppliers import models as suppliers_models
from backend.modules.inventory import models as inventory_models

# ==========================================================
# Alembic Config
# ==========================================================
config = context.config

# Se usi un file alembic.ini con sqlalchemy.url
# lo sovrascriviamo con DATABASE_URL dalle settings del progetto
from core.config import settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret logging.ini file se presente
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata
target_metadata = Base.metadata

# ==========================================================
# Funzioni run_migrations
# ==========================================================

def run_migrations_offline():
    """Esegui migrazioni in modalità offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Esegui migrazioni in modalità online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
