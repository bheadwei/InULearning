/**
 * API 工具函數
 * 提供統一的 API 調用接口
 */

// API 基礎配置
const API_CONFIG = {
    baseURL: 'http://localhost', // 生產環境應使用實際域名
    endpoints: {
        auth: ':8001',
        learning: ':8002',
        content: ':8003'
    }
};

// HTTP 請求工具類
class APIClient {
    constructor() {
        this.token = localStorage.getItem('access_token');
    }

    // 設置認證 Token
    setToken(token) {
        this.token = token;
        localStorage.setItem('access_token', token);
    }

    // 清除認證 Token
    clearToken() {
        this.token = null;
        localStorage.removeItem('access_token');
    }

    // 獲取請求標頭
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    // 通用請求方法
    async request(method, service, endpoint, data = null) {
        const url = `${API_CONFIG.baseURL}${API_CONFIG.endpoints[service]}${endpoint}`;

        const config = {
            method: method,
            headers: this.getHeaders(),
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, config);

            // 檢查 HTTP 狀態碼
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API 請求失敗:', error);
            throw error;
        }
    }

    // GET 請求
    async get(service, endpoint) {
        return this.request('GET', service, endpoint);
    }

    // POST 請求
    async post(service, endpoint, data) {
        return this.request('POST', service, endpoint, data);
    }

    // PUT 請求
    async put(service, endpoint, data) {
        return this.request('PUT', service, endpoint, data);
    }

    // DELETE 請求
    async delete(service, endpoint) {
        return this.request('DELETE', service, endpoint);
    }
}

// 創建全域 API 客戶端實例
const apiClient = new APIClient();

// 認證相關 API
const authAPI = {
    // 用戶註冊
    async register(userData) {
        return apiClient.post('auth', '/auth/register', userData);
    },

    // 用戶登入
    async login(credentials) {
        const response = await apiClient.post('auth', '/auth/login', credentials);
        if (response.data && response.data.access_token) {
            apiClient.setToken(response.data.access_token);
        }
        return response;
    },

    // 刷新 Token
    async refreshToken() {
        return apiClient.post('auth', '/auth/refresh', {});
    },

    // 獲取用戶資料
    async getProfile() {
        return apiClient.get('auth', '/auth/profile');
    },

    // 登出
    logout() {
        apiClient.clearToken();
    }
};

// 學習管理相關 API
const learningAPI = {
    // 生成題目
    async generateQuestions(requestData) {
        return apiClient.post('learning', '/learning/generate-questions', requestData);
    },

    // 提交答案
    async submitAnswer(answerData) {
        return apiClient.post('learning', '/learning/submit-answer', answerData);
    },

    // 獲取學習進度
    async getProgress(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/learning/progress?${queryString}` : '/learning/progress';
        return apiClient.get('learning', endpoint);
    },

    // 獲取相似題目
    async getSimilarQuestions(questionId, count = 5) {
        return apiClient.get('learning', `/learning/similar-questions?question_id=${questionId}&count=${count}`);
    }
};

// 內容管理相關 API
const contentAPI = {
    // 查詢題庫
    async getQuestions(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/content/questions?${queryString}` : '/content/questions';
        return apiClient.get('content', endpoint);
    },

    // 獲取學習資源
    async getLearningResources(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/content/learning-resources?${queryString}` : '/content/learning-resources';
        return apiClient.get('content', endpoint);
    },

    // 上傳檔案
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const url = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.content}/content/upload`;

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': apiClient.token ? `Bearer ${apiClient.token}` : undefined
            },
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }
};

// 工具函數
const utils = {
    // 顯示載入狀態
    showLoading(element) {
        element.innerHTML = '<div class="loading">載入中...</div>';
    },

    // 顯示錯誤訊息
    showError(element, message) {
        element.innerHTML = `<div class="error">錯誤: ${message}</div>`;
    },

    // 顯示成功訊息
    showSuccess(element, message) {
        element.innerHTML = `<div class="success">${message}</div>`;
    },

    // 格式化日期
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-TW', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // 格式化百分比
    formatPercentage(value) {
        return `${(value * 100).toFixed(1)}%`;
    }
};

// 匯出 API 和工具函數
window.authAPI = authAPI;
window.learningAPI = learningAPI;
window.contentAPI = contentAPI;
window.utils = utils; 