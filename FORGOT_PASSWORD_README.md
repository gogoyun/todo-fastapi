# 忘記密碼功能說明

## 功能概述

本專案已新增忘記密碼功能，包含以下兩個主要 API 端點：

1. **忘記密碼請求** (`POST /forgot-password`)
2. **重設密碼** (`POST /reset-password`)

## API 端點詳細說明

### 1. 忘記密碼請求

**端點**: `POST /forgot-password`

**請求格式**:
```json
{
  "email": "user@example.com"
}
```

**回應格式**:
```json
{
  "code": 200,
  "message": "密碼重設郵件已發送",
  "data": null
}
```

**功能**:
- 檢查電子郵件是否存在於資料庫中。
- 如果存在，則生成唯一的重設 token，儲存到資料庫（有效期 1 小時），並發送重設郵件。
- 如果不存在，則不執行任何操作。
- 為防止用戶枚舉攻擊，無論電子郵件是否存在，API 都會回傳相同的成功訊息。

### 2. 重設密碼

**端點**: `POST /reset-password`

**請求格式**:
```json
{
  "token": "your_reset_token_here",
  "new_password": "newpassword123"
}
```

**回應格式**:
```json
{
  "code": 200,
  "message": "密碼重設成功",
  "data": null
}
```

**功能**:
- 驗證重設 token 是否有效且未過期
- 更新用戶密碼
- 標記 token 為已使用

## 資料庫變更

新增了 `password_reset_tokens` 資料表，包含以下欄位：

- `id`: 主鍵
- `email`: 用戶郵箱
- `token`: 重設 token
- `expires_at`: 過期時間
- `used`: 是否已使用 (0=未使用, 1=已使用)
- `created_at`: 建立時間

## 使用流程

1. **用戶請求重設密碼**:
   - 用戶在前端輸入郵箱地址
   - 前端呼叫 `/forgot-password` API
   - 系統生成重設 token 並發送郵件

2. **用戶重設密碼**:
   - 用戶點擊郵件中的重設連結
   - 前端從 URL 參數中取得 token
   - 用戶輸入新密碼
   - 前端呼叫 `/reset-password` API
   - 系統驗證 token 並更新密碼

## 安全性考量

1. **Token 安全性**:
   - 使用 `secrets.token_urlsafe(32)` 生成安全的隨機 token
   - Token 有效期為 1 小時
   - Token 只能使用一次

2. **密碼安全性**:
   - 新密碼會經過 bcrypt 雜湊處理
   - 密碼長度限制為 6-8 字元

3. **用戶枚舉保護**:
   - `POST /forgot-password` 端點無論提交的電子郵件是否存在，都會回傳相同的成功回應，以防止攻擊者透過回傳的狀態來猜測哪些用戶是註冊用戶。

4. **錯誤處理**:
   - 無效的 token 會回傳適當的錯誤訊息
   - 過期的 token 會被自動清理

## 郵件發送設定

目前郵件發送功能為模擬模式，會在控制台輸出重設連結。

要啟用實際的郵件發送功能，請：

1. 在 `auth.py` 中取消註解郵件發送程式碼
2. 設定 SMTP 伺服器資訊
3. 設定發送者郵箱和應用程式密碼

範例 SMTP 設定（Gmail）:
```python
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'your-app-password')
```

## 測試

使用提供的測試腳本 `test_forgot_password.py` 來測試功能：

```bash
python tests/test_forgot_password.py
```

## 注意事項

1. 確保資料庫已更新（執行 `Base.metadata.create_all(bind=engine)`）
2. 在生產環境中，請設定適當的 SMTP 伺服器
3. 考慮使用 Redis 等快取系統來儲存 token，提高效能
4. 可以考慮增加重設密碼的頻率限制，防止濫用


## 生產環境測試

你可以使用 `tests/test_production.py` 來測試部署在 Render 或其他生產環境的忘記密碼 API：

```bash
python tests/test_production.py
```

- 請依照指示輸入實際的測試郵箱。
- 測試腳本會自動呼叫 `/forgot-password` 並檢查郵件發送狀態。
- 適合用於部署後的 smoke test 或驗證郵件服務設定。
