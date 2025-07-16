"""
學習管理服務主應用
處理依需求出題、自動批改、學習進度追蹤、相似題練習
支援 US-002, US-003, US-005, US-006
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import random

# 應用設定
app = FastAPI(
    title="InULearning 學習管理服務",
    description="處理依需求出題、自動批改、學習進度追蹤、相似題練習",
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
class GenerateQuestionsRequest(BaseModel):
    subject: str
    grade: int
    difficulty: str
    question_count: int
    focus_areas: Optional[List[str]] = None


class Question(BaseModel):
    question_id: str
    content: str
    type: str
    options: Optional[List[str]] = None
    difficulty: str
    subject_area: str


class GenerateQuestionsResponse(BaseModel):
    session_id: str
    questions: List[Question]


class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    user_answer: str
    time_spent: Optional[int] = None


class SubmitAnswerResponse(BaseModel):
    submission_id: str
    is_correct: bool
    correct_answer: str
    explanation: str
    score: int
    feedback: str


class LearningProgressResponse(BaseModel):
    overall_progress: Dict[str, Any]
    subject_progress: List[Dict[str, Any]]


class SimilarQuestionsResponse(BaseModel):
    similar_questions: List[Dict[str, Any]]


# 模擬題庫資料
SAMPLE_QUESTIONS = {
    "mathematics": {
        "algebra": [
            {
                "question_id": "math_001",
                "content": "解方程式 2x + 3 = 7",
                "type": "multiple_choice",
                "options": ["x=1", "x=2", "x=3", "x=4"],
                "correct_answer": "x=2",
                "explanation": "將 3 移到等號右邊得到 2x = 4，再除以 2 得到 x = 2",
                "difficulty": "medium"
            },
            {
                "question_id": "math_002",
                "content": "化簡 3x + 2x - x",
                "type": "short_answer",
                "correct_answer": "4x",
                "explanation": "合併同類項：3x + 2x - x = (3+2-1)x = 4x",
                "difficulty": "easy"
            }
        ],
        "geometry": [
            {
                "question_id": "math_003",
                "content": "計算半徑為 5 的圓面積",
                "type": "short_answer",
                "correct_answer": "25π",
                "explanation": "圓面積公式 A = πr²，所以 A = π × 5² = 25π",
                "difficulty": "medium"
            }
        ]
    }
}


# API 端點
@app.post("/learning/generate-questions", response_model=GenerateQuestionsResponse)
async def generate_questions(request: GenerateQuestionsRequest):
    """
    依需求生成題目 (US-002)
    根據學科、年級、難度生成個人化題目
    """
    # 驗證輸入
    if request.subject not in SAMPLE_QUESTIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subject '{request.subject}' not supported"
        )
    
    if request.difficulty not in ["easy", "medium", "hard"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Difficulty must be one of: easy, medium, hard"
        )
    
    if not 1 <= request.question_count <= 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question count must be between 1 and 50"
        )
    
    # 生成會話 ID
    session_id = str(uuid.uuid4())
    
    # 從題庫選擇題目
    questions = []
    subject_data = SAMPLE_QUESTIONS[request.subject]
    
    for topic, topic_questions in subject_data.items():
        if request.focus_areas and topic not in request.focus_areas:
            continue
        
        for q in topic_questions:
            if q["difficulty"] == request.difficulty and len(questions) < request.question_count:
                question = Question(
                    question_id=q["question_id"],
                    content=q["content"],
                    type=q["type"],
                    options=q.get("options"),
                    difficulty=q["difficulty"],
                    subject_area=topic
                )
                questions.append(question)
    
    # 如果題目不足，重複選擇
    while len(questions) < request.question_count:
        for topic, topic_questions in subject_data.items():
            if len(questions) >= request.question_count:
                break
            for q in topic_questions:
                if len(questions) >= request.question_count:
                    break
                question = Question(
                    question_id=f"{q['question_id']}_{len(questions)}",
                    content=q["content"],
                    type=q["type"],
                    options=q.get("options"),
                    difficulty=q["difficulty"],
                    subject_area=topic
                )
                questions.append(question)
    
    return GenerateQuestionsResponse(
        session_id=session_id,
        questions=questions[:request.question_count]
    )


@app.post("/learning/submit-answer", response_model=SubmitAnswerResponse)
async def submit_answer(request: SubmitAnswerRequest):
    """
    提交答案並自動批改 (US-003)
    自動批改學生答案並提供回饋
    """
    # 查找正確答案（模擬從題庫查詢）
    correct_answer = None
    explanation = None
    
    # 從模擬題庫中查找答案
    for subject_data in SAMPLE_QUESTIONS.values():
        for topic_questions in subject_data.values():
            for q in topic_questions:
                if q["question_id"] == request.question_id:
                    correct_answer = q["correct_answer"]
                    explanation = q["explanation"]
                    break
            if correct_answer:
                break
        if correct_answer:
            break
    
    if not correct_answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # 判斷答案是否正確
    is_correct = request.user_answer.strip().lower() == correct_answer.lower()
    score = 100 if is_correct else 0
    
    # 生成回饋
    if is_correct:
        feedback = "回答正確！很好的表現。"
    else:
        feedback = f"回答錯誤。正確答案是 {correct_answer}。建議重新複習相關概念。"
    
    return SubmitAnswerResponse(
        submission_id=str(uuid.uuid4()),
        is_correct=is_correct,
        correct_answer=correct_answer,
        explanation=explanation,
        score=score,
        feedback=feedback
    )


@app.get("/learning/progress", response_model=LearningProgressResponse)
async def get_learning_progress(
    subject: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    查詢學習進度 (US-006)
    返回學生的學習進度和統計資料
    """
    # 模擬學習進度資料
    overall_progress = {
        "total_questions": 150,
        "correct_answers": 120,
        "accuracy_rate": 0.8,
        "study_time_minutes": 1200
    }
    
    subject_progress = [
        {
            "subject": "mathematics",
            "mastery_level": 0.75,
            "topics": [
                {
                    "topic": "algebra",
                    "mastery_level": 0.85,
                    "last_practiced": datetime.utcnow().isoformat()
                },
                {
                    "topic": "geometry",
                    "mastery_level": 0.65,
                    "last_practiced": datetime.utcnow().isoformat()
                }
            ]
        }
    ]
    
    # 如果指定學科，過濾結果
    if subject:
        subject_progress = [sp for sp in subject_progress if sp["subject"] == subject]
    
    return LearningProgressResponse(
        overall_progress=overall_progress,
        subject_progress=subject_progress
    )


@app.get("/learning/similar-questions", response_model=SimilarQuestionsResponse)
async def get_similar_questions(
    question_id: str,
    count: int = 5
):
    """
    獲取相似題目 (US-005)
    根據原題目找出相似的練習題
    """
    if not 1 <= count <= 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Count must be between 1 and 20"
        )
    
    # 模擬相似題目生成
    similar_questions = []
    
    for i in range(count):
        similar_question = {
            "question_id": f"similar_{question_id}_{i+1}",
            "content": f"類似題目 {i+1}：解方程式 {2+i}x + {3+i} = {7+i}",
            "type": "multiple_choice",
            "difficulty": "medium",
            "similarity_score": 0.85 - (i * 0.05)
        }
        similar_questions.append(similar_question)
    
    return SimilarQuestionsResponse(
        similar_questions=similar_questions
    )


@app.get("/learning/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "service": "learning", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 