import asyncio
import getpass
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

tenant_id = input("Tenant ID: ")
client_id = input("Client ID: ")
client_secret = getpass.getpass("Client Secret (hidden): ")

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

client = GraphServiceClient(credentials=credential)

async def main():
    upn = input("User principal name to delete: ")
    await client.users.by_user_id(upn).delete()
    print(f"Deleted: {upn}")

asyncio.run(main())
