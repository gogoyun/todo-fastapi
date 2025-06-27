#!/usr/bin/env python3
"""
測試忘記密碼功能的腳本
"""

import requests
import json

# API 基礎 URL
BASE_URL = "http://localhost:8000"

def test_forgot_password():
    """測試忘記密碼功能"""
    print("=== 測試忘記密碼功能 ===")
    
    # 1. 測試已註冊的電子郵件
    print("\n1. 測試已註冊的電子郵件...")
    registered_email = "test@example.com"  # 假設這個用戶已註冊
    forgot_data = {
        "email": registered_email
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forgot-password", json=forgot_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200 and "如果您的電子郵件存在於我們的系統中" in response.json().get("message", ""):
            print(f"✅ 對已註冊郵件 {registered_email} 的請求成功")
        else:
            print(f"❌ 對已註冊郵件 {registered_email} 的請求失敗")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到伺服器，請確保 FastAPI 伺服器正在運行")
        return
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

    # 2. 測試未註冊的電子郵件
    print("\n2. 測試未註冊的電子郵件...")
    unregistered_email = "nonexistent@example.com"
    forgot_data_unregistered = {
        "email": unregistered_email
    }
    
    try:
        response_unregistered = requests.post(f"{BASE_URL}/forgot-password", json=forgot_data_unregistered)
        print(f"狀態碼: {response_unregistered.status_code}")
        print(f"回應: {response_unregistered.json()}")
        
        if response_unregistered.status_code == 200 and "如果您的電子郵件存在於我們的系統中" in response_unregistered.json().get("message", ""):
            print(f"✅ 對未註冊郵件 {unregistered_email} 的請求成功 (預期行為)")
        else:
            print(f"❌ 對未註冊郵件 {unregistered_email} 的請求失敗")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到伺服器，請確保 FastAPI 伺服器正在運行")
        return
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

def test_reset_password():
    """測試重設密碼功能（需要有效的 token）"""
    print("\n=== 測試重設密碼功能 ===")
    print("注意: 這個測試需要有效的 token，通常從忘記密碼郵件中獲得")
    
    # 這裡需要一個有效的 token，實際使用時會從郵件中獲得
    reset_data = {
        "token": "your_reset_token_here",
        "new_password": "newpass123"
    }
    
    print("請手動測試重設密碼功能，使用從郵件中獲得的 token")

if __name__ == "__main__":
    print("開始測試忘記密碼功能...")
    test_forgot_password()
    # test_reset_password() # 這個通常需要手動操作
    print("\n測試完成！") 