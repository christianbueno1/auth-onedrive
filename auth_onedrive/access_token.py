from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv
from azure.core.credentials import TokenCredential, AccessToken

load_dotenv()

# Azure AD app details
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


async def get_access_token():
    # Create a ConfidentialClientApplication instance
    app: ConfidentialClientApplication = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority="https://login.microsoftonline.com/" + TENANT_ID,
        client_credential=CLIENT_SECRET
    )
    print("App created.")
    scopes = ["https://graph.microsoft.com/.default"]
    # Acquire a token for the current confidential client (app-only)
    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        access_token = result["access_token"]
        # print("Access token acquired:", access_token)
        return access_token
    else:
        print(f"Error: {result.get('error')}")
        print(f"Error: {result.get('error_description')}")
        return None
    
class AsyncTokenCredential(TokenCredential):
    def __init__(self, token):
        self.token = token

    async def get_token(self, *scopes, **kwargs):
        return AccessToken(self.token, 0)
    
    def close(self):
        pass