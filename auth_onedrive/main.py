# use MSAL Python to get access token for Microsoft Graph
import msal
import os
from dotenv import load_dotenv

load_dotenv()

def run():

    # Azure AD app details
    TENANT_ID = os.getenv("TENANT_ID")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    AUTHORITY = "https://login.microsoftonline.com/" + TENANT_ID

    # Create a confidential client application
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )
# acquire a token on behalf of a user
    accounts = app.get_accounts()

# if there are no accounts in the cache, the user must sign in
    if accounts:
        result = app.acquire_token_silent(["User.Read"], account=accounts[0])
    else:
        result = app.acquire_token_on_behalf_of(["User.Read"])
    if "access_token" in result:
        print(f"Access token: {result['access_token']}")
    else:
        print(f"Authentication failed: {result.get('error_description')}")



if __name__ == "__main__":
    run()
