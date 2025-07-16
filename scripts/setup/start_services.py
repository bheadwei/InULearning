#!/usr/bin/env python3
"""
InULearning 第一階段 MVP 服務啟動腳本
啟動認證服務、學習管理服務、內容管理服務
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

# 服務配置
SERVICES = {
    'auth': {
        'name': '認證服務',
        'path': 'backend/services/auth',
        'port': 8001,
        'health_endpoint': '/auth/health'
    },
    'learning': {
        'name': '學習管理服務',
        'path': 'backend/services/learning',
        'port': 8002,
        'health_endpoint': '/learning/health'
    },
    'content': {
        'name': '內容管理服務',
        'path': 'backend/services/content',
        'port': 8003,
        'health_endpoint': '/content/health'
    }
}

def print_banner():
    """顯示啟動橫幅"""
    print("=" * 60)
    print("  InULearning 個人化學習平台 - 第一階段 MVP")
    print("=" * 60)
    print("正在啟動核心服務...")
    print()

def check_python_version():
    """檢查 Python 版本"""
    if sys.version_info < (3, 8):
        print("❌ 錯誤: 需要 Python 3.8 或更高版本")
        sys.exit(1)
    print(f"✅ Python 版本: {sys.version}")

def check_dependencies():
    """檢查必要依賴"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ 依賴套件檢查通過")
    except ImportError as e:
        print(f"❌ 缺少依賴套件: {e}")
        print("請執行: pip install -r requirements.txt")
        sys.exit(1)

def start_service(service_name, config):
    """啟動單個服務"""
    print(f"🚀 啟動 {config['name']} (端口 {config['port']})...")
    
    # 切換到服務目錄
    service_path = Path(config['path'])
    if not service_path.exists():
        print(f"❌ 服務目錄不存在: {service_path}")
        return None
    
    # 啟動服務
    cmd = [
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", str(config['port']),
        "--reload"
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            cwd=service_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待服務啟動
        time.sleep(3)
        
        # 檢查服務是否正常運行
        if process.poll() is None:
            print(f"✅ {config['name']} 啟動成功")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ {config['name']} 啟動失敗")
            print(f"錯誤: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ 啟動 {config['name']} 時發生錯誤: {e}")
        return None

def check_service_health(service_name, config):
    """檢查服務健康狀態"""
    url = f"http://localhost:{config['port']}{config['health_endpoint']}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {config['name']} 健康檢查通過")
            return True
        else:
            print(f"❌ {config['name']} 健康檢查失敗 (HTTP {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {config['name']} 健康檢查失敗: {e}")
        return False

def main():
    """主函數"""
    print_banner()
    
    # 檢查環境
    check_python_version()
    check_dependencies()
    
    # 啟動服務
    processes = {}
    
    for service_name, config in SERVICES.items():
        process = start_service(service_name, config)
        if process:
            processes[service_name] = process
        else:
            print(f"❌ 無法啟動 {config['name']}，退出...")
            # 終止已啟動的服務
            for p in processes.values():
                p.terminate()
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("等待服務完全啟動...")
    time.sleep(5)
    
    # 健康檢查
    print("\n🔍 執行健康檢查...")
    all_healthy = True
    
    for service_name, config in SERVICES.items():
        if not check_service_health(service_name, config):
            all_healthy = False
    
    if all_healthy:
        print("\n🎉 所有服務啟動成功！")
        print("\n📋 服務狀態:")
        for service_name, config in SERVICES.items():
            print(f"  • {config['name']}: http://localhost:{config['port']}")
        
        print("\n🌐 API 文檔:")
        for service_name, config in SERVICES.items():
            print(f"  • {config['name']}: http://localhost:{config['port']}/docs")
        
        print("\n📱 前端應用:")
        print("  • 學生端: 請開啟 frontend/student/index.html")
        
        print("\n💡 第一階段 MVP 功能:")
        print("  ✅ US-001: 會員註冊與登入")
        print("  ✅ US-002: 依需求出題")
        print("  ✅ US-003: 自動批改與分析")
        print("  ✅ US-004: 錯題相關資源")
        print("  ✅ US-005: 相似題練習")
        print("  ✅ US-006: 學習歷程記錄")
        
        print("\n按 Ctrl+C 停止所有服務")
        
        try:
            # 保持服務運行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 正在停止服務...")
            for service_name, process in processes.items():
                print(f"停止 {SERVICES[service_name]['name']}...")
                process.terminate()
                process.wait()
            print("✅ 所有服務已停止")
    else:
        print("\n❌ 部分服務啟動失敗，請檢查錯誤訊息")
        # 終止所有服務
        for process in processes.values():
            process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main() 