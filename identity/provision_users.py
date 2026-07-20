import asyncio
import csv
import getpass
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.user import User
from msgraph.generated.models.password_profile import PasswordProfile

tenant_id = input("Tenant ID: ")
client_id = input("Client ID: ")
client_secret = getpass.getpass("Client Secret (hidden): ")
domain = input("Tenant domain: ")
temp_password = getpass.getpass("Temporary password for all new users (hidden): ")

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

client = GraphServiceClient(credentials=credential)

async def create_user(row):
    first = row["first_name"]
    last = row["last_name"]
    mail_nickname = f"{first}.{last}".lower()
    upn = f"{mail_nickname}@{domain}"

    new_user = User(
        account_enabled=True,
        display_name=f"{first} {last}",
        mail_nickname=mail_nickname,
        user_principal_name=upn,
        department=row["department"],
        job_title=row["job_title"],
        password_profile=PasswordProfile(
            force_change_password_next_sign_in=True,
            password=temp_password,
        ),
    )

    try:
        await client.users.post(new_user)
        print(f"  Created: {upn}  ({row['license_tier']})")
    except Exception as e:
        print(f"  Skipped: {upn}  — {e}")

async def main():
    with open("identity/users.csv") as f:
        rows = list(csv.DictReader(f))

    print(f"Provisioning {len(rows)} users...")
    for row in rows:
        await create_user(row)
    print("Done.")

asyncio.run(main())
