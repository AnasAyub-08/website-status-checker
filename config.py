import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:GiFCrvKokTPcOCdHzsgaVLBFXfSZjcPO@postgres.railway.internal:5432/railway")
    SQLALCHEMY_TRACK_MODIFICATIONS = False