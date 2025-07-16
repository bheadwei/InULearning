"""
PostgreSQL 資料庫連接管理
用於處理用戶資料、學習記錄、分析結果等結構化資料
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .config import db_settings

# 建立資料庫引擎
engine = create_engine(
    db_settings.database_url,
    pool_size=db_settings.db_pool_size,
    max_overflow=db_settings.db_max_overflow,
    pool_timeout=db_settings.db_pool_timeout,
    pool_pre_ping=True,
    echo=False  # 生產環境設為 False
)

# 建立 Session 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立基礎模型類別
Base = declarative_base()


def get_db():
    """取得資料庫會話"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """建立所有資料表"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """刪除所有資料表"""
    Base.metadata.drop_all(bind=engine) 