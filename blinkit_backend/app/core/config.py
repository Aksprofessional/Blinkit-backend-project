import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)
    )
    SECRET_KEY_CURSOR: str =os.getenv("SECRET_KEY_CURSOR")
    MAIL_USERNAME = os.getenv(
    "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    MAIL_FROM = os.getenv(
        "MAIL_FROM"
    )

    MAIL_PORT = int(
        os.getenv(
            "MAIL_PORT",
            587,
        )
    )

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER"
    )

    MAIL_STARTTLS = (
        os.getenv(
            "MAIL_STARTTLS",
            "True",
        )
        == "True"
    )

    MAIL_SSL_TLS = (
        os.getenv(
            "MAIL_SSL_TLS",
            "False",
        )
        == "True"
    )



Setting=Settings()