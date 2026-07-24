from fastapi_mail import ConnectionConfig

from app.core.config import Setting

conf = ConnectionConfig(
    MAIL_USERNAME=Setting.MAIL_USERNAME,
    MAIL_PASSWORD=Setting.MAIL_PASSWORD,
    MAIL_FROM=Setting.MAIL_FROM,
    MAIL_PORT=Setting.MAIL_PORT,
    MAIL_SERVER=Setting.MAIL_SERVER,
    MAIL_STARTTLS=Setting.MAIL_STARTTLS,
    MAIL_SSL_TLS=Setting.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
)