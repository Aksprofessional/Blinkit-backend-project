from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings



engine = create_engine(
    settings.DATABASE_URL,
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

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

