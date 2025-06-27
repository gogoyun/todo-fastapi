# Render 部署指南

## 🚀 部署到 Render

本專案已準備好部署到 Render 平台，支援完整的忘記密碼郵件發送功能。

## 📋 部署前準備

### 1. 環境變數設定

在 Render 控制台中設定以下環境變數：

#### 必要變數
- `SECRET_KEY`: JWT 密鑰（Render 會自動生成）
- `DATABASE_URL`: PostgreSQL 連接字串（Render 會自動設定）
- `ENVIRONMENT`: 設為 `production`

#### 郵件設定（Gmail 範例）
- `SMTP_SERVER`: `smtp.gmail.com`
- `SMTP_PORT`: `587`
- `SMTP_USERNAME`: 你的 Gmail 帳號
- `SMTP_PASSWORD`: Gmail 應用程式密碼
- `SMTP_FROM_EMAIL`: 發送者郵箱（可與 SMTP_USERNAME 相同）

#### 應用程式設定
- `APP_URL`: 你的前端應用程式 URL（例如：`https://your-frontend-app.onrender.com`）

### 2. Gmail 應用程式密碼設定

1. 前往 [Google 帳戶設定](https://myaccount.google.com/)
2. 開啟「兩步驟驗證」
3. 前往「應用程式密碼」
4. 生成新的應用程式密碼
5. 將此密碼設定為 `SMTP_PASSWORD`

## 🔧 部署步驟

### 方法一：使用 render.yaml（推薦）

1. 將程式碼推送到 GitHub
2. 在 Render 中連接 GitHub 倉庫
3. 選擇「Blueprint」部署方式
4. Render 會自動讀取 `render.yaml` 並設定所有服務

### 方法二：手動部署

1. 在 Render 中建立新的 Web Service
2. 連接 GitHub 倉庫
3. 設定以下參數：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. 手動設定所有環境變數

## 📧 郵件發送測試

部署完成後，可以使用以下方式測試郵件發送：

### 1. 使用測試腳本
```bash
# 修改測試腳本中的 BASE_URL
BASE_URL = "https://your-app-name.onrender.com"
python tests/test_complete_flow.py
```

### 2. 使用 curl 命令
```bash
# 測試忘記密碼
curl -X POST "https://your-app-name.onrender.com/forgot-password" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

## 🔍 故障排除

### 常見問題

1. **郵件發送失敗**
   - 檢查 SMTP 設定是否正確
   - 確認 Gmail 應用程式密碼是否有效
   - 檢查防火牆設定

2. **資料庫連接失敗**
   - 確認 `DATABASE_URL` 是否正確
   - 檢查 PostgreSQL 服務是否正常

3. **CORS 錯誤**
   - 確認 `APP_URL` 設定正確
   - 檢查前端 URL 是否在允許清單中

### 日誌查看

在 Render 控制台的「Logs」標籤中查看應用程式日誌，可以幫助診斷問題。

## 🔒 安全性注意事項

1. **環境變數**: 不要在程式碼中硬編碼敏感資訊
2. **HTTPS**: Render 自動提供 HTTPS
3. **資料庫**: 使用 Render 的 PostgreSQL 服務
4. **郵件**: 使用應用程式密碼而非一般密碼

## 📈 監控和維護

1. **健康檢查**: 定期檢查應用程式狀態
2. **日誌監控**: 監控錯誤日誌
3. **效能監控**: 關注回應時間和資源使用
4. **備份**: 定期備份資料庫

## 🎯 部署檢查清單

- [ ] 所有環境變數已設定
- [ ] Gmail 應用程式密碼已生成
- [ ] 前端 URL 已正確設定
- [ ] 資料庫已連接
- [ ] 郵件發送功能已測試
- [ ] CORS 設定正確
- [ ] HTTPS 正常工作

## 📞 支援

如果遇到部署問題，可以：
1. 檢查 Render 官方文件
2. 查看應用程式日誌
3. 確認環境變數設定
4. 測試郵件發送功能 