from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    user_name: str = None
    pass_word: str = None
    host: str = None
   
    class Config:
      env_file = ".env"

settings = Settings()