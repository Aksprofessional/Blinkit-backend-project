from cloudinary import uploader
from fastapi import HTTPException,status,UploadFile





ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

def validate_image(image:UploadFile):
    if image.content_type is None or image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed."
        )

#uploading a file to cloudinary and getting the link
def upload_image(image: UploadFile):
    validate_image(image)
    try:
        result = uploader.upload(image.file, folder="products")
        public_id = result["public_id"]
        image_url = result["secure_url"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image upload failed: {str(e)}"
        )
    print(result)

    return{
        "url":image_url,
        "public_id":public_id
    }




def destroy_image(public_id):

    try:
        uploader.destroy(public_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"old image could not be deleted: {str(e)}"
        )



