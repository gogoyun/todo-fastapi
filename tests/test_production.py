#!/usr/bin/env python3
"""
生產環境測試腳本
用於測試部署到 Render 後的忘記密碼功能
"""

import requests
import json
import os

# 從環境變數或手動設定 API 基礎 URL
BASE_URL = os.getenv("API_BASE_URL", "https://your-app-name.onrender.com")

def test_health_check():
    """測試應用程式健康狀態"""
    print("=== 測試應用程式健康狀態 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 應用程式正常運行")
            return True
        else:
            print("❌ 應用程式無法訪問")
            return False
            
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        return False

def test_forgot_password_production():
    """測試生產環境的忘記密碼功能"""
    print("\n=== 測試生產環境忘記密碼功能 ===")
    
    # 請輸入實際的測試郵箱
    test_email = input("請輸入測試郵箱地址: ").strip()
    
    if not test_email:
        print("未輸入郵箱地址，跳過測試")
        return False
    
    forgot_data = {
        "email": test_email
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forgot-password", json=forgot_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 忘記密碼請求成功")
            print("請檢查郵箱是否收到重設密碼郵件")
            return True
        else:
            print("❌ 忘記密碼請求失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def test_reset_password_production():
    """測試生產環境的重設密碼功能"""
    print("\n=== 測試生產環境重設密碼功能 ===")
    
    token = input("請輸入從郵件中獲得的重設 token: ").strip()
    new_password = input("請輸入新密碼 (6-8字元): ").strip()
    
    if not token or not new_password:
        print("未輸入必要資訊，跳過測試")
        return False
    
    reset_data = {
        "token": token,
        "new_password": new_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/reset-password", json=reset_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 密碼重設成功")
            return True
        else:
            print("❌ 密碼重設失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def main():
    """主測試函數"""
    print(f"開始測試生產環境 API: {BASE_URL}")
    print("=" * 50)
    
    # 1. 健康檢查
    if not test_health_check():
        print("應用程式無法訪問，停止測試")
        return
    
    # 2. 忘記密碼測試
    test_forgot_password_production()
    
    # 3. 重設密碼測試（可選）
    print("\n是否要測試重設密碼功能？(y/n): ", end="")
    choice = input().strip().lower()
    
    if choice == 'y':
        test_reset_password_production()
    
    print("\n=== 測試完成 ===")
    print("如果忘記密碼功能正常工作，你應該收到一封包含重設連結的郵件")

if __name__ == "__main__":
    main() 