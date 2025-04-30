# FastAPI Todo + 會員系統

這是一個使用 FastAPI、SQLAlchemy 與 SQLite 打造的 Todo 應用程式，  
支援會員註冊、登入（JWT）、Todo CRUD，並且所有 API 回傳皆統一格式。

---

## 功能特色

- 會員註冊（Email、姓名、密碼，密碼長度6-8碼）
- 會員登入（JWT Token）
- Todo 新增、查詢、更新、刪除（需登入）
- 密碼加密儲存（bcrypt）
- API 回傳統一格式（含 code、message、data）

---

## 安裝與啟動

1. **安裝套件**

   ```bash
   pip install -r requirements.txt
   ```

2. **啟動伺服器**

   ```bash
   uvicorn main:app --reload
   ```

3. **開啟 API 文件**

   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
     使用 Swagger UI 測試所有 API

---

## API 使用方式

### 1. 註冊

- **POST** `/register`
- Body (JSON)：
  ```json
  {
    "email": "your@email.com",
    "password": "123456",
    "name": "你的名字"
  }
  ```

### 2. 登入

- **POST** `/login`
- Body (JSON)：
  ```json
  {
    "email": "your@email.com",
    "password": "123456"
  }
  ```
- 回傳：
  ```json
  {
    "code": 200,
    "message": "登入成功",
    "data": {
      "access_token": "xxx",
      "token_type": "bearer"
    }
  }
  ```

### 3. 取得 Todo 列表

- **GET** `/todos`
- Header: `Authorization: Bearer <access_token>`

### 4. 新增 Todo

- **POST** `/todos`
- Body (JSON)：
  ```json
  {
    "title": "任務標題"
  }
  ```

### 5. 更新 Todo

- **PUT** `/todos/{todo_id}`
- Body (JSON)：
  ```json
  {
    "title": "新標題"
  }
  ```

### 6. 刪除 Todo

- **DELETE** `/todos/{todo_id}`

---

## 密碼加密規則

- 密碼長度必須為 6~8 碼。
- 密碼在註冊時會使用 **bcrypt** 演算法進行雜湊加密，**不會以明碼儲存**。
- 登入時會將輸入密碼與資料庫中的 bcrypt 雜湊進行比對驗證。

---

## 資料庫

- 使用 SQLite (`todo.db`)，可用 DB Browser for SQLite 或 VSCode SQLite 插件檢視內容。

---

## 部署到 Render

- 請確保 `requirements.txt`、`main.py` 都在專案根目錄。
- Render 的啟動指令建議：
  ```
  uvicorn main:app --host 0.0.0.0 --port 10000
  ```

---

## 聯絡方式

如有問題，歡迎提 issue 或聯絡作者。

---

如需更詳細的 API 文件，請參考 `/docs` 自動產生的 Swagger UI。
