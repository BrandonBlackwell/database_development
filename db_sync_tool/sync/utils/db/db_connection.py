# db_sync_tool/sync/utils/db_connections.py
"""
Minimal helper functions to create SQLAlchemy Engine instances for dev and prod.
Adjust connection URL defaults or environment variables to match your setup.
"""

from typing import Optional
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def _default_url_for(db_type: str, purpose: str) -> Optional[str]:
    """
    Return a sensible default URL for common DB types. `purpose` is 'dev' or 'prod'.
    Override by setting environment variables:
      DEV_DB_URL or PROD_DB_URL
    or more specific:
      DEV_MARIA_URL, PROD_MARIA_URL, DEV_SQLITE_URL, etc.
    """
    env_generic = os.environ.get(f"{purpose.upper()}_DB_URL")
    if env_generic:
        return env_generic

    env_specific = os.environ.get(f"{purpose.upper()}_{db_type.upper()}_URL")
    if env_specific:
        return env_specific

    if db_type in ("sqlite", "sqlite3"):
        # file-based sqlite defaults (dev uses local file, prod should be explicit)
        return os.environ.get(f"{purpose.upper()}_SQLITE_URL", "sqlite:///./dev.db" if purpose == "dev" else None)
    if db_type in ("maria", "mysql"):
        # example DSN using PyMySQL driver; replace with real credentials or env vars
        return os.environ.get(
            f"{purpose.upper()}_MARIA_URL",
            "mysql+pymysql://user:pass@localhost/dev_db" if purpose == "dev" else None,
        )
    if db_type in ("postgres", "postgresql"):
        return os.environ.get(
            f"{purpose.upper()}_POSTGRES_URL",
            "postgresql+psycopg2://user:pass@localhost/dev_db" if purpose == "dev" else None,
        )
    return None


def create_dev_db_engine(url: Optional[str] = None, db_type: str = "maria") -> Engine:
    """
    Create and return a SQLAlchemy Engine for development use.

    - url: optional SQLAlchemy URL. If not provided, environment variables are consulted.
    - db_type: one of 'maria', 'mysql', 'sqlite', 'postgres', etc. Used to pick defaults.
    """
    resolved = url or _default_url_for(db_type, "dev")
    if not resolved:
        raise ValueError("No development DB URL provided. Set DEV_DB_URL or pass `url`.")
    # Keep defaults lightweight for dev
    return create_engine(resolved, echo=False, pool_pre_ping=True)


def create_prod_db_engine(url: Optional[str] = None, db_type: str = "maria") -> Engine:
    """
    Create and return a SQLAlchemy Engine for production use.

    - url: required (unless PROD_DB_URL or PROD_<DBTYPE>_URL env var is set).
    - db_type: used only to pick environment defaults if url is None.
    """
    resolved = url or _default_url_for(db_type, "prod")
    if not resolved:
        raise ValueError("No production DB URL provided. Set PROD_DB_URL or pass `url`.")
    # More robust pool settings for production
    return create_engine(
        resolved,
        echo=False,
        pool_pre_ping=True,
        pool_size=int(os.environ.get("PROD_POOL_SIZE", 10)),
        max_overflow=int(os.environ.get("PROD_MAX_OVERFLOW", 20)),
    )