"""
認證服務主應用
處理用戶註冊、登入、JWT 管理、權限控制
支援 US-001: 會員註冊與登入
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# 應用設定
app = FastAPI(
    title="InULearning 認證服務",
    description="處理用戶註冊、登入、JWT 管理、權限控制",
    version="1.0.0"
)

# CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應設定具體域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT 設定
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# 密碼加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer Token 認證
security = HTTPBearer()


# Pydantic 模型
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    grade: Optional[int] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict


class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    role: str
    grade: Optional[int] = None
    created_at: str


# 工具函數
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """密碼加密"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """建立 JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """驗證 JWT Token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# API 端點
@app.post("/auth/register", response_model=UserResponse)
async def register(user_data: UserRegister):
    """
    用戶註冊 (US-001)
    支援學生、家長、老師多角色註冊
    """
    # 驗證角色
    valid_roles = ["student", "parent", "teacher"]
    if user_data.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be one of: student, parent, teacher"
        )
    
    # 學生必須提供年級
    if user_data.role == "student" and not user_data.grade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Grade is required for student role"
        )
    
    # 密碼加密
    hashed_password = get_password_hash(user_data.password)
    
    # 這裡應該連接資料庫儲存用戶
    # 暫時返回模擬資料
    user_response = UserResponse(
        user_id="uuid-123",
        username=user_data.username,
        email=user_data.email,
        role=user_data.role,
        grade=user_data.grade,
        created_at=datetime.utcnow().isoformat()
    )
    
    return user_response


@app.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """
    用戶登入 (US-001)
    返回 JWT Token 用於後續認證
    """
    # 這裡應該從資料庫驗證用戶
    # 暫時使用模擬邏輯
    if user_credentials.email == "test@example.com" and user_credentials.password == "password":
        # 建立 JWT Token
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        access_token = create_access_token(
            data={"sub": "uuid-123", "role": "student"},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="Bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_HOURS * 3600,
            user={
                "user_id": "uuid-123",
                "username": "test_user",
                "email": user_credentials.email,
                "role": "student"
            }
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/auth/refresh", response_model=dict)
async def refresh_token(token_data: dict = Depends(verify_token)):
    """
    刷新 JWT Token
    """
    # 建立新的 Token
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    new_token = create_access_token(
        data={"sub": token_data["sub"], "role": token_data["role"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": new_token,
        "expires_in": ACCESS_TOKEN_EXPIRE_HOURS * 3600
    }


@app.get("/auth/profile", response_model=dict)
async def get_profile(token_data: dict = Depends(verify_token)):
    """
    獲取用戶資料
    """
    # 這裡應該從資料庫查詢用戶資料
    # 暫時返回模擬資料
    return {
        "user_id": token_data["sub"],
        "username": "test_user",
        "email": "test@example.com",
        "role": token_data["role"],
        "grade": 7 if token_data["role"] == "student" else None,
        "is_active": True
    }


@app.get("/auth/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "service": "auth", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 