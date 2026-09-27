from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_grpc_port: int = 6334
    qdrant_collection: str = "episodic_priors"
    agent_id: str = "default_agent"
    
    class Config:
        env_file = ".env"

settings = Settings()
