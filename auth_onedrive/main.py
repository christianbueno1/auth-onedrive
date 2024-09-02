import asyncio

from auth_onedrive.onedrive_auth import main


def app():
  asyncio.run(main())