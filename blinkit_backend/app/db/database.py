from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import Setting



# Create the SQLAlchemy engine with connection pool configuration
engine = create_engine(
    Setting.DATABASE_URL,
    pool_size=20,  # Phase 1.5: 20 persistent connections (supports 100+ users)
    max_overflow=30,  # Max 50 total connections (supports 300-500 concurrent users)
    pool_recycle=3600,
    pool_pre_ping=True,  # Verify connections before use
    pool_timeout=5,  # CRITICAL: Fail fast for real-time trading (reduced from 30s)
    echo=False,
    connect_args={
        "connect_timeout": 10,  # Database connection timeout
        "options": "-c statement_timeout=30000"  # 30s query timeout
    }
)

# Create a session factory for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy ORM models
Base = declarative_base()

# Dependency that provides a database session for each request
def get_db():

    # Create a new database session
    db = SessionLocal()
    try:

        # Yield the session to the requesting endpoint
        yield db
    finally:

        # Ensure the session is closed after the request completes
        db.close()