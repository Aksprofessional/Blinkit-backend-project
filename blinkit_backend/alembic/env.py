from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 1. Import your dynamic database configurations and base models
from app.db.database import Base
from app.core.config import Setting  # Injects your database config setup

# 2. Explicitly import all 9 models so Alembic can track them for autogeneration
from app.models.user import User
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.category import Category
from app.models.products import Products
from app.models.product_variant import product_variant
from app.models.delivery_address import delivery_address
from app.models.order_items import order_items
from app.models.orders import order
from app.models.sub_category import SubCategory
from app.models.brand import brand

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Bind the models metadata tracking
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Overwrite offline URL with your active Python environment string
    url = Setting.DATABASE_URL
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Fetch the template dictionary block from alembic.ini
    alembic_config = config.get_section(config.config_ini_section, {})
    
    # Overwrite the placeholder string with your real dynamic connection url
    alembic_config["sqlalchemy.url"] = Setting.DATABASE_URL

    connectable = engine_from_config(
        alembic_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
