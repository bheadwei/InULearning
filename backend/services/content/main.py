"""
內容管理服務主應用
處理題庫管理、學習資源、多媒體內容
支援 US-004: 錯題相關資源
"""

from fastapi import FastAPI, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# 應用設定
app = FastAPI(
    title="InULearning 內容管理服務",
    description="處理題庫管理、學習資源、多媒體內容",
    version="1.0.0"
)

# CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 模型
class QuestionResponse(BaseModel):
    question_id: str
    content: str
    type: str
    subject: str
    grade: int
    difficulty: str
    topic: str
    tags: List[str]


class LearningResourceResponse(BaseModel):
    resource_id: str
    title: str
    type: str
    url: str
    description: str
    duration: Optional[int] = None
    file_size: Optional[int] = None


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    file_url: str
    file_size: int
    content_type: str


# 模擬資料
SAMPLE_RESOURCES = [
    {
        "resource_id": "res_001",
        "title": "一元一次方程式教學影片",
        "type": "video",
        "url": "https://example.com/videos/algebra_001.mp4",
        "description": "詳細解說一元一次方程式的解法",
        "duration": 300,
        "subject": "mathematics",
        "topic": "algebra"
    },
    {
        "resource_id": "res_002",
        "title": "代數基礎概念筆記",
        "type": "document",
        "url": "https://example.com/docs/algebra_notes.pdf",
        "description": "代數基礎概念整理筆記",
        "file_size": 2048000,
        "subject": "mathematics",
        "topic": "algebra"
    },
    {
        "resource_id": "res_003",
        "title": "圓的面積公式說明",
        "type": "image",
        "url": "https://example.com/images/circle_area.png",
        "description": "圓面積公式的圖解說明",
        "file_size": 512000,
        "subject": "mathematics",
        "topic": "geometry"
    }
]


# API 端點
@app.get("/content/questions", response_model=List[QuestionResponse])
async def get_questions(
    subject: Optional[str] = None,
    grade: Optional[int] = None,
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    page: int = 1,
    page_size: int = 20
):
    """
    查詢題庫
    支援多條件過濾和分頁
    """
    # 驗證分頁參數
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than 0"
        )
    
    if not 1 <= page_size <= 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be between 1 and 100"
        )
    
    # 模擬題庫查詢
    questions = [
        QuestionResponse(
            question_id="q001",
            content="解方程式 2x + 3 = 7",
            type="multiple_choice",
            subject="mathematics",
            grade=7,
            difficulty="medium",
            topic="algebra",
            tags=["equation", "algebra", "basic"]
        ),
        QuestionResponse(
            question_id="q002",
            content="計算半徑為 5 的圓面積",
            type="short_answer",
            subject="mathematics",
            grade=7,
            difficulty="medium",
            topic="geometry",
            tags=["circle", "area", "geometry"]
        ),
        QuestionResponse(
            question_id="q003",
            content="化簡 3x + 2x - x",
            type="short_answer",
            subject="mathematics",
            grade=7,
            difficulty="easy",
            topic="algebra",
            tags=["simplify", "algebra", "basic"]
        )
    ]
    
    # 應用過濾條件
    filtered_questions = questions
    
    if subject:
        filtered_questions = [q for q in filtered_questions if q.subject == subject]
    
    if grade:
        filtered_questions = [q for q in filtered_questions if q.grade == grade]
    
    if difficulty:
        filtered_questions = [q for q in filtered_questions if q.difficulty == difficulty]
    
    if topic:
        filtered_questions = [q for q in filtered_questions if q.topic == topic]
    
    # 分頁處理
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    return filtered_questions[start_index:end_index]


@app.get("/content/learning-resources", response_model=List[LearningResourceResponse])
async def get_learning_resources(
    question_id: Optional[str] = None,
    subject: Optional[str] = None,
    topic: Optional[str] = None,
    type: Optional[str] = None
):
    """
    獲取學習資源 (US-004)
    提供與錯題相關的影片、筆記、圖片等學習資源
    """
    # 驗證資源類型
    if type and type not in ["video", "document", "image"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type must be one of: video, document, image"
        )
    
    # 模擬資源查詢
    resources = []
    
    for resource_data in SAMPLE_RESOURCES:
        # 應用過濾條件
        if subject and resource_data.get("subject") != subject:
            continue
        
        if topic and resource_data.get("topic") != topic:
            continue
        
        if type and resource_data["type"] != type:
            continue
        
        resource = LearningResourceResponse(
            resource_id=resource_data["resource_id"],
            title=resource_data["title"],
            type=resource_data["type"],
            url=resource_data["url"],
            description=resource_data["description"],
            duration=resource_data.get("duration"),
            file_size=resource_data.get("file_size")
        )
        resources.append(resource)
    
    return resources


@app.post("/content/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    上傳多媒體內容
    支援圖片、影片、文檔等格式
    """
    # 驗證檔案類型
    allowed_types = {
        "image/jpeg", "image/png", "image/gif",
        "video/mp4", "video/avi",
        "application/pdf", "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed"
        )
    
    # 驗證檔案大小 (10MB 限制)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 10MB limit"
        )
    
    # 模擬檔案儲存
    file_id = str(uuid.uuid4())
    file_url = f"https://storage.example.com/uploads/{file_id}_{file.filename}"
    
    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_url=file_url,
        file_size=len(file_content),
        content_type=file.content_type
    )


@app.get("/content/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "service": "content", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 