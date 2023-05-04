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
    OPEN_AI_TOKEN_URL = "https://ai-testing-izazj9yw.authentication.sap.hana.ondemand.com/oauth/token"
    OPEN_AI_CLIENT_ID = "sb-88ed59fc-b6c1-4b12-9895-aa2faf36078d!b75280|azure-openai-service-i057149-xs!b16730"
    OPEN_AI_CLIENT_SECRET = "046f55bd-74c6-458f-afe0-5dc7935b7375$o8CL8xCc3TX79WcUdj9rieNv-DCuMRAP48-whaZha18="
    OPEN_AI_SVC_URL = "https://azure-openai-serv-i057149.cfapps.sap.hana.ondemand.com"
    OPEN_AI_TIMEOUT = 5000
