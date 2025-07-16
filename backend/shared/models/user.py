"""
用戶資料模型
支援多角色用戶系統：學生、家長、老師
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from ..database.postgresql import Base


class UserRole(enum.Enum):
    """用戶角色枚舉"""
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"


class User(Base):
    """用戶資料表"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    grade = Column(Integer, nullable=True)  # 學生年級
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role.value}')>"
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            "user_id": str(self.id),
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "grade": self.grade,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 