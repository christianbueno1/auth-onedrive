# use MSAL Python to get access token for Microsoft Graph
import msal
import os
from dotenv import load_dotenv
from msgraph import GraphServiceClient

load_dotenv()

def run():

    # Azure AD app details
    TENANT_ID = os.getenv("TENANT_ID")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    AUTHORITY = "https://login.microsoftonline.com/" + TENANT_ID
    # SCOPES = ['https://graph.microsoft.com/.default']
    SCOPES = ["User.Read"]

    # use the PublicClientApplication class to authenticate with Azure AD
    # Initialize the msal application object
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY
    )
    # Initialize device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if 'user_code' in flow:
        print(flow['message'])
    else:
        raise ValueError('Fail to create device flow')
    # Acquire a token using the device code flow
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        # print(f"Access token: {result['access_token']}")
        print(f"Access token: ok")
    else:
        print(f"Authentication failed: {result.get('error_description')}")
    
    # create graph_client using GraphServiceClient class and the access token
    # graph_client = GraphServiceClient(credential=AccessTokenCredential(result['access_token']))


if __name__ == "__main__":
    run()
