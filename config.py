import os


class Config:
    # Generative AI View
    CONTEXT_PATH = os.environ.get("CONTEXT_PATH")
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME", "")

    # Vision One internal API communication
    SSO_URL = os.environ.get("SSO_URL", "")
    JWT_URL = os.environ.get("JWT_URL", "")
    JWT_TIMEOUT = eval(os.environ.get("JWT_TIMEOUT", "5000"))
    JWT_SECRET = os.environ.get("CONSTANTS_JWT_SECRET", "")
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "")
    SSO_DEBUG = os.environ.get("SSO_DEBUG", "")

    # Open AI integration
    OPEN_AI_TOKEN_URL = os.environ.get("OPEN_AI_TOKEN_URL", "")
    OPEN_AI_CLIENT_ID = os.environ.get("OPEN_AI_CLIENT_ID", "")
    OPEN_AI_CLIENT_SECRET = os.environ.get("OPEN_AI_CLIENT_SECRET", "")
    OPEN_AI_SVC_URL = os.environ.get("OPEN_AI_SVC_URL", "")
    OPEN_AI_TIMEOUT = eval(os.environ.get("OPEN_AI_TIMEOUT", "5000"))
