import traceback
import asyncio
from dotenv import load_dotenv
from msgraph import GraphServiceClient

from auth_onedrive.access_token import get_access_token, AsyncTokenCredential

load_dotenv()

# SCOPES = ['https://graph.microsoft.com/.default', 'User.Read', 'Files.Read.All']
# SCOPES = ['User.Read', 'Files.Read.All']
SCOPES = ['User.Read']

async def get_onedrive_info(token: AsyncTokenCredential):
    try:

        # Create a GraphServiceClient object with delegated permissions
        client = GraphServiceClient(credentials=token, scopes=SCOPES)
        print("Client created.")



        # Get user information (optional)
        user = await client.me.get()
        print(f"User: {user.display_name}")

        
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


async def main():
    token = await get_access_token()
    if token:
      print(f"Access token acquired: {token}")
      credential = AsyncTokenCredential(token)
      print(f"Credential created: {credential}")
      await get_onedrive_info(credential)
    else:
      print("Failed to connect to OneDrive.")

  
if __name__ == "__main__":
    asyncio.run(main())