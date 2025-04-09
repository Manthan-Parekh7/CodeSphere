from django.conf import settings
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from google.oauth2.credentials import Flow

# Define OAuth 2.0 scopes
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

def get_google_oauth_flow():
    return Flow.from_client_secrets_file(
        'client_secrets.json',  # You'll need to download this from Google Cloud Console
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI
    )

def verify_google_id_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            settings.GOOGLE_OAUTH_CLIENT_ID
        )
        return idinfo
    except ValueError:
        return None
