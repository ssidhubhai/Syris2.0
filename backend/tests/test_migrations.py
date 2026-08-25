import uuid
import os
import pytest
from alembic import command
from alembic.config import Config

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALEMBIC_INI_PATH = os.path.join(BACKEND_DIR, "alembic.ini")


def test_alembic_upgrade_downgrade_smoke():
    """Smoke test ensuring Alembic configuration and migration scripts execute without errors."""
    alembic_cfg = Config(ALEMBIC_INI_PATH)
    alembic_cfg.set_main_option("script_location", os.path.join(BACKEND_DIR, "migrations"))
    
    # Use temporary test database for migration smoke test with unique id
    temp_db_path = os.path.join(BACKEND_DIR, f"test_migration_temp_{uuid.uuid4().hex[:8]}.db")
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)
    
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{temp_db_path}")

    try:
        # Upgrade to head
        command.upgrade(alembic_cfg, "head")
        
        # Downgrade to base
        command.downgrade(alembic_cfg, "base")
        
        # Upgrade back to head
        command.upgrade(alembic_cfg, "head")
    finally:
        if os.path.exists(temp_db_path):
            try:
                os.remove(temp_db_path)
            except PermissionError:
                pass
