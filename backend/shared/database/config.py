"""
資料庫配置模組
支援 PostgreSQL, MongoDB, Redis, Milvus 多資料庫架構
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """資料庫設定"""
    
    # PostgreSQL 設定
    database_url: str = "postgresql://inulearning:password@localhost:5432/inulearning"
    
    # MongoDB 設定
    mongodb_url: str = "mongodb://localhost:27017/inulearning"
    mongodb_database: str = "inulearning"
    
    # Redis 設定
    redis_url: str = "redis://localhost:6379/0"
    
    # Milvus 設定
    milvus_host: str = "localhost"
    milvus_port: int = 19530
    milvus_collection_name: str = "question_vectors"
    
    # 連接池設定
    db_pool_size: int = 20
    db_max_overflow: int = 0
    db_pool_timeout: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 全域設定實例
db_settings = DatabaseSettings() 