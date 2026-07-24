from fastapi_mail import FastMail
from fastapi_mail import MessageSchema
from fastapi_mail import MessageType

from app.core.mail import conf


async def send_verification_email(
    email: str,
    token: str,
):
    verify_link = (
        f"http://127.0.0.1:8000/auth/verify-email?token={token}"
    )

    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"""
Hello,

Click the link below to verify your account.

{verify_link}

If you didn't create this account, ignore this email.
""",
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)

    await fm.send_message(message)