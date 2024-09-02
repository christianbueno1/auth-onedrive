import asyncio

from auth_onedrive.onedrive_auth import main


def app():
  print("Hello from auth_onedrive!")
  asyncio.run(main())