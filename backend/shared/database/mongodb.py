"""
MongoDB 資料庫連接管理
用於處理題庫、學習資源等非結構化資料
"""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from .config import db_settings


class MongoDBManager:
    """MongoDB 連接管理器"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
    
    async def connect(self):
        """建立 MongoDB 連接"""
        self.client = AsyncIOMotorClient(db_settings.mongodb_url)
        self.database = self.client[db_settings.mongodb_database]
        
        # 測試連接
        try:
            await self.client.admin.command('ping')
            print("MongoDB 連接成功")
        except Exception as e:
            print(f"MongoDB 連接失敗: {e}")
            raise
    
    async def disconnect(self):
        """關閉 MongoDB 連接"""
        if self.client:
            self.client.close()
    
    def get_collection(self, collection_name: str):
        """取得指定集合"""
        if not self.database:
            raise RuntimeError("MongoDB 未連接")
        return self.database[collection_name]
    
    async def create_indexes(self):
        """建立索引"""
        # 題目集合索引
        questions_collection = self.get_collection("questions")
        await questions_collection.create_index("question_id", unique=True)
        await questions_collection.create_index([("subject", 1), ("grade", 1)])
        await questions_collection.create_index([("difficulty", 1), ("topic", 1)])
        
        # 學習資源集合索引
        resources_collection = self.get_collection("learning_resources")
        await resources_collection.create_index("resource_id", unique=True)
        await resources_collection.create_index([("subject", 1), ("topic", 1)])


# 全域 MongoDB 管理器實例
mongodb_manager = MongoDBManager() 