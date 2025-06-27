#!/usr/bin/env python3
"""
完整的用戶認證流程測試腳本
包含註冊、登入、忘記密碼和重設密碼
"""

import requests
import json
import time

# API 基礎 URL
BASE_URL = "http://localhost:8000"

def test_register():
    """測試用戶註冊"""
    print("=== 測試用戶註冊 ===")
    
    register_data = {
        "email": "test@example.com",
        "password": "123456",
        "name": "測試用戶"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=register_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 用戶註冊成功")
            return True
        else:
            print("❌ 用戶註冊失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def test_login():
    """測試用戶登入"""
    print("\n=== 測試用戶登入 ===")
    
    login_data = {
        "email": "test@example.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 用戶登入成功")
            return True
        else:
            print("❌ 用戶登入失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def test_forgot_password():
    """測試忘記密碼功能"""
    print("\n=== 測試忘記密碼功能 ===")
    
    forgot_data = {
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forgot-password", json=forgot_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200 and "如果您的電子郵件存在於我們的系統中" in response.json().get("message", ""):
            print("✅ 忘記密碼請求成功")
            return True
        else:
            print("❌ 忘記密碼請求失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def test_forgot_password_nonexistent_user():
    """測試對不存在的用戶請求忘記密碼"""
    print("\n=== 測試對不存在的用戶請求忘記密碼 ===")
    
    forgot_data = {
        "email": "nonexistent@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forgot-password", json=forgot_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200 and "如果您的電子郵件存在於我們的系統中" in response.json().get("message", ""):
            print("✅ 對不存在的用戶請求忘記密碼成功 (預期行為)")
            return True
        else:
            print("❌ 對不存在的用戶請求忘記密碼失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def test_reset_password_with_invalid_token():
    """測試使用無效 token 重設密碼"""
    print("\n=== 測試使用無效 token 重設密碼 ===")
    
    reset_data = {
        "token": "invalid_token_here",
        "new_password": "newpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/reset-password", json=reset_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 400:
            print("✅ 無效 token 被正確拒絕")
            return True
        else:
            print("❌ 無效 token 沒有被正確處理")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def test_login_with_old_password():
    """測試使用舊密碼登入（應該失敗）"""
    print("\n=== 測試使用舊密碼登入 ===")
    
    login_data = {
        "email": "test@example.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 舊密碼仍然有效")
            return True
        else:
            print("❌ 舊密碼登入失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def main():
    """執行完整測試流程"""
    print("開始完整用戶認證流程測試...")
    
    # 1. 註冊用戶
    if not test_register():
        print("註冊失敗，停止測試")
        return
    
    # 2. 登入測試
    test_login()
    
    # 3. 忘記密碼測試
    if not test_forgot_password():
        print("忘記密碼失敗，停止測試")
        return
    
    # 4. 測試對不存在的用戶請求忘記密碼
    if not test_forgot_password_nonexistent_user():
        print("對不存在的用戶請求忘記密碼失敗，停止測試")
        return
    
    # 5. 測試無效 token
    test_reset_password_with_invalid_token()
    
    # 6. 測試舊密碼是否仍然有效
    test_login_with_old_password()
    
    print("\n=== 測試完成 ===")
    print("注意：要測試實際的重設密碼功能，請：")
    print("1. 查看伺服器控制台輸出的重設連結")
    print("2. 從連結中取得 token")
    print("3. 使用該 token 呼叫 /reset-password API")

if __name__ == "__main__":
    main() 