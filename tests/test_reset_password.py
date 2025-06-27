#!/usr/bin/env python3
"""
手動測試重設密碼功能
"""

import requests
import json

# API 基礎 URL
BASE_URL = "http://localhost:8000"

def test_forgot_password_and_get_token():
    """測試忘記密碼並取得 token"""
    print("=== 測試忘記密碼並取得 token ===")
    
    forgot_data = {
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forgot-password", json=forgot_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 忘記密碼請求成功")
            print("請查看伺服器控制台輸出的重設連結")
            return True
        else:
            print("❌ 忘記密碼請求失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def test_reset_password_with_token(token):
    """使用指定的 token 測試重設密碼"""
    print(f"\n=== 使用 token 重設密碼 ===")
    print(f"Token: {token}")
    
    reset_data = {
        "token": token,
        "new_password": "newpass"
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

def test_login_with_new_password():
    """測試使用新密碼登入"""
    print("\n=== 測試使用新密碼登入 ===")
    
    login_data = {
        "email": "test@example.com",
        "password": "newpass"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 新密碼登入成功")
            return True
        else:
            print("❌ 新密碼登入失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        return False

def main():
    """主測試函數"""
    print("開始手動測試重設密碼功能...")
    
    # 1. 請求忘記密碼
    if not test_forgot_password_and_get_token():
        return
    
    # 2. 等待用戶輸入 token
    print("\n請從伺服器控制台複製重設連結中的 token，然後輸入：")
    token = input("請輸入重設 token: ").strip()
    
    if not token:
        print("未輸入 token，停止測試")
        return
    
    # 3. 使用 token 重設密碼
    if not test_reset_password_with_token(token):
        return
    
    # 4. 測試新密碼登入
    test_login_with_new_password()
    
    print("\n=== 測試完成 ===")

if __name__ == "__main__":
    main() 