import asyncio
import os
from dotenv import load_dotenv
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.drives.item.items.items_request_builder import ItemsRequestBuilder
from msgraph.generated.models.drive_item import DriveItem

load_dotenv()

# Azure AD app details
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPES = ['https://graph.microsoft.com/.default']

async def get_client():
    credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    client = GraphServiceClient(credentials=credentials, scopes=SCOPES)
    return client

async def list_files(client):
    try:
        # Correct method to list files in the root directory
        print(f"client: {client}\n")
        drive_items = await client.me.drive.root.children.get()
        for item in drive_items:
            print(item.name)
    except Exception as e:
        print(f"An error occurred: {e}")

async def upload_file(client, file_path, file_name):
    with open(file_path, 'rb') as upload_file:
        file_content = upload_file.read()

    drive_item = DriveItem()
    drive_item.name = file_name

    uploaded_item = await client.me.drive.root.children.post(drive_item)
    upload_session = await client.me.drive.items[uploaded_item.id].create_upload_session.post()

    # For simplicity, we're uploading the entire file at once.
    # For larger files, you should implement chunked upload.
    await client.drives[uploaded_item.parent_reference.drive_id].items[uploaded_item.id].upload_session.put(content=file_content)

    print(f"File uploaded: {file_name}")

async def download_file(client, file_name, local_path):
    items = await client.me.drive.root.children.get()
    file_to_download = next((item for item in items.value if item.name == file_name), None)

    if file_to_download:
        content = await client.me.drive.items[file_to_download.id].content.get()
        with open(local_path, 'wb') as file:
            file.write(content)
        print(f"File downloaded: {local_path}")
    else:
        print(f"File not found: {file_name}")

async def main():
    client = await get_client()

    print("Listing files:")
    await list_files(client)

    # print("\nUploading file:")
    # await upload_file(client, "path/to/local/file.txt", "uploaded_file.txt")

    # print("\nDownloading file:")
    # await download_file(client, "uploaded_file.txt", "path/to/downloaded_file.txt")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())