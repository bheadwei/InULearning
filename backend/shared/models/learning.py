"""
學習相關資料模型
包含學習進度、答題記錄、AI 分析結果
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database.postgresql import Base


class LearningProgress(Base):
    """學習進度表"""
    __tablename__ = "learning_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    subject = Column(String(50), nullable=False)
    topic = Column(String(100), nullable=False)
    mastery_level = Column(Numeric(3, 2), default=0.0)  # 掌握度 0-1
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    last_practiced = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<LearningProgress(user_id='{self.user_id}', subject='{self.subject}', topic='{self.topic}')>"
    
    def to_dict(self):
        return {
            "progress_id": str(self.id),
            "user_id": str(self.user_id),
            "subject": self.subject,
            "topic": self.topic,
            "mastery_level": float(self.mastery_level) if self.mastery_level else 0.0,
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "accuracy_rate": self.correct_answers / self.total_questions if self.total_questions > 0 else 0.0,
            "last_practiced": self.last_practiced.isoformat() if self.last_practiced else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class AnswerSubmission(Base):
    """答題記錄表"""
    __tablename__ = "answer_submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    question_id = Column(String(100), nullable=False)
    session_id = Column(String(100), nullable=True)
    user_answer = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    score = Column(Integer, default=0)  # 0-100
    time_spent = Column(Integer, nullable=True)  # 秒
    feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AnswerSubmission(user_id='{self.user_id}', question_id='{self.question_id}')>"
    
    def to_dict(self):
        return {
            "submission_id": str(self.id),
            "user_id": str(self.user_id),
            "question_id": self.question_id,
            "session_id": self.session_id,
            "user_answer": self.user_answer,
            "correct_answer": self.correct_answer,
            "is_correct": self.is_correct,
            "score": self.score,
            "time_spent": self.time_spent,
            "feedback": self.feedback,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
        }


class AIAnalysisResult(Base):
    """AI 分析結果表"""
    __tablename__ = "ai_analysis_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    analysis_type = Column(String(50), nullable=False)  # weakness, recommendation, similarity
    status = Column(String(20), default="processing")  # processing, completed, failed
    input_data = Column(JSONB, nullable=True)
    result_data = Column(JSONB, nullable=True)
    confidence_score = Column(Numeric(3, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<AIAnalysisResult(user_id='{self.user_id}', analysis_type='{self.analysis_type}')>"
    
    def to_dict(self):
        return {
            "analysis_id": str(self.id),
            "user_id": str(self.user_id),
            "analysis_type": self.analysis_type,
            "status": self.status,
            "input_data": self.input_data,
            "result_data": self.result_data,
            "confidence_score": float(self.confidence_score) if self.confidence_score else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        } 