import cloudinary
import cloudinary.uploader
from config.config import (
    CLOUDYNARY_API_KEY, CLOUDYNARY_SECRET_KEY, CLOUDYNARY_CLOUD_NAME)

cloudinary.config(
    cloud_name=CLOUDYNARY_CLOUD_NAME,
    api_key=CLOUDYNARY_API_KEY,
    api_secret=CLOUDYNARY_SECRET_KEY
)


class UploadService:
    def __init__(self) -> None:
        print("Cloudinary Uploading Cloud is generated")

    def upload_file(self, file, folder="uploads/") -> str | None:
        try:
            print("Uploading file...")
            result = cloudinary.uploader.upload(file, folder=folder)
            print(f"File uploaded successfully: {result.get('url')}")
            return result.get('url')
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None
