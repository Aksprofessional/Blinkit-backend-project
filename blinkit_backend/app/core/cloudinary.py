import cloudinary
from app.core.config import Setting

cloudinary.config(
    cloud_name=Setting.CLOUDINARY_CLOUD_NAME,
    api_key=Setting.CLOUDINARY_API_KEY,
    api_secret=Setting.CLOUDINARY_API_SECRET,
    secure=True,
)