"""
Redis 快取管理
用於快取熱點資料、會話管理、臨時計算結果
"""

import redis
from typing import Optional, Any
import json
from .config import db_settings


class RedisManager:
    """Redis 連接管理器"""
    
    def __init__(self):
        self.client: Optional[redis.Redis] = None
    
    def connect(self):
        """建立 Redis 連接"""
        self.client = redis.from_url(db_settings.redis_url, decode_responses=True)
        
        # 測試連接
        try:
            self.client.ping()
            print("Redis 連接成功")
        except Exception as e:
            print(f"Redis 連接失敗: {e}")
            raise
    
    def disconnect(self):
        """關閉 Redis 連接"""
        if self.client:
            self.client.close()
    
    def set_cache(self, key: str, value: Any, expire: int = 3600):
        """設定快取"""
        if not self.client:
            raise RuntimeError("Redis 未連接")
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        
        self.client.set(key, value, ex=expire)
    
    def get_cache(self, key: str) -> Optional[Any]:
        """取得快取"""
        if not self.client:
            raise RuntimeError("Redis 未連接")
        
        value = self.client.get(key)
        if value is None:
            return None
        
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    def delete_cache(self, key: str):
        """刪除快取"""
        if not self.client:
            raise RuntimeError("Redis 未連接")
        
        self.client.delete(key)
    
    def set_session(self, session_id: str, user_data: dict, expire: int = 86400):
        """設定用戶會話"""
        key = f"session:{session_id}"
        self.set_cache(key, user_data, expire)
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """取得用戶會話"""
        key = f"session:{session_id}"
        return self.get_cache(key)
    
    def delete_session(self, session_id: str):
        """刪除用戶會話"""
        key = f"session:{session_id}"
        self.delete_cache(key)


# 全域 Redis 管理器實例
redis_manager = RedisManager() 