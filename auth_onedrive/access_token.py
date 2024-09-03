import msal
import os
from dotenv import load_dotenv
from azure.core.credentials import TokenCredential, AccessToken
from azure.identity.aio import DefaultAzureCredential

load_dotenv()

# Azure AD app details


async def get_access_token():
    tenant_id = os.getenv("TENANT_ID")
    authority = "https://login.microsoftonline.com/" + tenant_id
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    scope = ["User.Read"]

    # Create a confidential client application
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )
    print("App created.")

    # scopes = ["https://graph.microsoft.com/.default"]
    # Acquire a token for the current confidential client (app-only)
    # result = app.acquire_token_for_client(scopes=scopes)

     # Get the authorization URL
    auth_url = app.get_authorization_request_url(scope, redirect_uri=redirect_uri)
    print(f"Please go to this URL and authorize the application: {auth_url}")

    # Wait for the user to complete the authorization
    input("Press Enter after authorizing the application...")

    # Read the authorization code from the file
    with open("auth_code.txt", "r") as f:
        auth_code = f.read().strip()

    # Acquire a token using the authorization code
    result = app.acquire_token_by_authorization_code(auth_code, scopes=scope, redirect_uri=redirect_uri)

    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Failed to acquire token: {result.get('error_description')}")
        return None
    
    
class AsyncTokenCredential(TokenCredential):
    def __init__(self, token):
        self.token = token
        self._credentials = DefaultAzureCredential()

    async def get_token(self, *scopes, **kwargs):
        return AccessToken(self.token, 0)
    
    async def close(self):
        await self._credentials.close()