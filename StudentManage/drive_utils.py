from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
import pickle
from googleapiclient.http import MediaFileUpload

def upload_to_drive(file_path, file_name):
    token_path = os.path.join(os.path.dirname(__file__), "../token.pickle")
    if not os.path.exists(token_path):
        return "User not authenticated"

    with open(token_path, "rb") as token:
        creds = pickle.load(token)

    drive_service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": file_name}
    media = MediaFileUpload(file_path, mimetype="application/octet-stream")

    file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()

    return file.get("id")
