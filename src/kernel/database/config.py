from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    database_url: str
    DEBUG: bool = False

    @property 
    def DATABASE_URL_asyncpg(self) -> str: 
        """DSN string for async engine (asyncpg)"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property 
    def DATABASE_URL_psycopg(self) -> str: 
        """DSN string for sync engine (psycopg2/psycopg3)"""
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env") 


settings = Settings()
