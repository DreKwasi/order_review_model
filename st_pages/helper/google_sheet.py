import gspread
from google.oauth2 import service_account
from decouple import config

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]


cred = {
    "type": config("type"),
    "project_id": config("project_id"),
    "private_key_id": config("private_key_id"),
    "private_key": config('private_key'),
    "client_email": config("client_email"),
    "client_id": config("client_id"),
    "auth_uri": config("auth_uri"),
    "token_uri": config("token_uri"),
    "auth_provider_x509_cert_url": config("auth_provider_x509_cert_url"),
    "client_x509_cert_url": config("client_x509_cert_url")
}
credentials = service_account.Credentials.from_service_account_info(
    cred, scopes=scope)
client = gspread.authorize(credentials)
client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1AE03fmOuEe8ik5Kl2mW9Ziv0bs6jgeqNqltUp2o7C2E/edit?pli=1#gid=1171120654")
