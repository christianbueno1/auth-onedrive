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
        # user = await client.me.get()
        # print("User information:")
        # print(user)
        
        drive = await client.me.drive.get()
        if drive:
            print(f"Drive information: {drive}")
        else:
            print("Failed to retrieve drive information.")

        # # Get OneDrive information
        # drive = await client.drive().get()
        # print("OneDrive information:")
        # print(drive)

        # # Get a list of files in the root folder (optional)
        # files = await client.drive("root").children().get()
        # if files:
        #     print("Files in the root folder:")
        #     for file in files.value:
        #         print(file)
        # else:
        #     print("Failed to retrieve files in the root folder.")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error: {e.args}")


async def main():
    token = await get_access_token()
    if token:
      credential = AsyncTokenCredential(token)
      await get_onedrive_info(credential)
    else:
      print("Failed to connect to OneDrive.")

  
if __name__ == "__main__":
    asyncio.run(main())