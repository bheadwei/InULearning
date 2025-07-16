# InULearning 個人化學習平台

## 專案概述
InULearning 是一個 AI 驅動的個人化學習平台，透過智能分析學習弱點、提供精準練習，並優化親子溝通，解決傳統教育無法兼顧個人差異的痛點。

## 技術架構
- **前端**: HTML/CSS/JavaScript + Ajax (多角色響應式設計)
- **後端**: FastAPI (Python 3.11+) 微服務架構
- **資料庫**: PostgreSQL + MongoDB + Redis + Milvus
- **AI 技術**: LangChain + Gemini API + RAG 架構
- **非同步處理**: Celery + RabbitMQ
- **容器化**: Docker
- **監控**: Langfuse + Ragas

## 資料夾結構

```
InULearning/
├── backend/                     # 後端微服務
│   ├── services/               # 核心微服務
│   │   ├── auth/              # 用戶認證服務
│   │   ├── learning/          # 學習管理服務
│   │   ├── ai_analysis/       # AI 分析服務
│   │   ├── content/           # 內容管理服務
│   │   ├── report/            # 報告服務
│   │   └── notification/      # 通知服務
│   └── shared/                # 共用模組
│       ├── database/          # 資料庫連接配置
│       ├── utils/             # 工具函數
│       ├── models/            # 共用資料模型
│       └── middleware/        # 中介軟體
├── frontend/                   # 前端應用
│   ├── student/               # 學生端 Web 應用
│   ├── parent/                # 家長端 Web 應用
│   ├── teacher/               # 老師端 Web 應用
│   └── shared/                # 共用前端資源
│       ├── components/        # 共用組件
│       ├── styles/            # 共用樣式
│       └── utils/             # 前端工具函數
├── infrastructure/             # 基礎設施配置
│   ├── docker/                # Docker 配置
│   ├── nginx/                 # Nginx 配置
│   └── monitoring/            # 監控配置
├── data/                      # 資料庫初始化
│   ├── postgresql/            # PostgreSQL 初始化腳本
│   ├── mongodb/               # MongoDB 初始化腳本
│   ├── redis/                 # Redis 配置
│   └── milvus/                # Milvus 配置
├── scripts/                   # 自動化腳本
│   ├── setup/                 # 環境設置腳本
│   ├── deployment/            # 部署腳本
│   └── migration/             # 資料庫遷移腳本
├── tests/                     # 測試套件
│   ├── unit/                  # 單元測試
│   ├── integration/           # 整合測試
│   └── e2e/                   # 端到端測試
├── docs/                      # 文檔
│   ├── api/                   # API 文檔
│   ├── deployment/            # 部署文檔
│   └── development/           # 開發文檔
├── requirements.txt           # Python 依賴
├── docker-compose.yml         # Docker Compose 配置
└── .env.example              # 環境變數範例
```

## 核心功能模組

### 用戶故事支援
- **US-001**: 會員註冊與登入
- **US-002**: 依需求出題
- **US-003**: 自動批改與分析
- **US-004**: 錯題相關資源
- **US-005**: 相似題練習
- **US-006**: 學習歷程記錄
- **US-007**: AI 智慧化升級
- **US-008**: 家長儀表板
- **US-009**: AI 溝通建議
- **US-010**: 班級儀表板

### 微服務架構
1. **認證服務** - 多角色用戶認證、JWT 管理、權限控制
2. **學習管理服務** - 依需求出題、自動批改、學習進度追蹤
3. **AI 分析服務** - 弱點分析、相似題生成、智能學習建議
4. **內容管理服務** - 題庫管理、學習資源、多媒體內容
5. **報告服務** - 生成學習報告、儀表板數據、數據視覺化
6. **通知服務** - 學習提醒、進度通知、家長溝通

## 開發階段

### 第一階段 MVP (2025-07-19)
- 完成核心學習與評量循環
- 會員系統、依需求出題、自動批改
- 錯題資源、相似題練習、學習歷程記錄

### 第二階段 MVP - 學生端 (2025-07-20)
- AI 智慧化升級：主動生成相似題與文字詳解

### 第二階段 MVP - 家長端 (2025-07-25)
- 家長儀表板上線：視覺化弱點分析與 AI 溝通建議

### 第二階段 MVP - 老師端 (2025-07-26)
- 班級儀表板建置：幫助老師掌握全班狀況，實現因材施教

## 快速開始

1. 環境設置
```bash
# 複製環境變數配置
cp .env.example .env

# 安裝 Python 依賴
pip install -r requirements.txt

# 啟動資料庫服務
docker-compose up -d postgresql mongodb redis milvus
```

2. 初始化資料庫
```bash
# 執行資料庫遷移
python scripts/setup/init_databases.py
```

3. 啟動服務
```bash
# 啟動所有微服務
docker-compose up
```

## 相關文檔
- [API 設計規範](docs/api/README.md)
- [部署指南](docs/deployment/README.md)
- [開發指南](docs/development/README.md)

## 授權
MIT License 