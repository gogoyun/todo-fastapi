from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 告訴 Pydantic Settings 去讀取 .env 檔案
    # extra='ignore' 表示如果 .env 有額外變數但模型未定義，則忽略
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

    secret_key: str
    algorithm: str = "HS256" # 常用於 JWT

settings = Settings()

# 可以做一個簡單的檢查
if not settings.secret_key:
    raise ValueError("SECRET_KEY environment variable not set in .env or environment.")