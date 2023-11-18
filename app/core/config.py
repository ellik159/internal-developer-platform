import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/idp")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
settings = Settings()
