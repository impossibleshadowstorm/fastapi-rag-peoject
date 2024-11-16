import boto3
from app.core.config import settings

def upload_to_s3(file):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3.upload_fileobj(file.file, settings.S3_BUCKET_NAME, file.filename)
    return f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
