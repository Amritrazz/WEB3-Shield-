from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    PROJECT_NAME: str = "Web3-Shield Backend"
    SECRET_KEY: str = "YOUR_SUPER_SECRET_JWT_KEY_CHANGE_THIS_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database URLs (Fed directly from Docker Compose / .env)
    DATABASE_URL: str = "postgresql://postgres:password123@postgres:5432/web3_shield"
    MONGO_URL: str = "mongodb://admin:secret123@mongodb:27017"
    REDIS_URL: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()