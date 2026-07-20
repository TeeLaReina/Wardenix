import asyncio
import getpass
import csv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.group import Group

tenant_id = input("Tenant ID: ")
client_id = input("Client ID: ")
client_secret = getpass.getpass("Client Secret (hidden): ")

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

client = GraphServiceClient(credentials=credential)

async def create_department_group(department):
    rule = f'(user.department -eq "{department}")'

    new_group = Group(
        display_name=f"{department} Team",
        mail_enabled=False,
        mail_nickname=department.lower().replace(" ", ""),
        security_enabled=True,
        group_types=["DynamicMembership"],
        membership_rule=rule,
        membership_rule_processing_state="On",
    )

    try:
        created = await client.groups.post(new_group)
        print(f"  Created: {created.display_name}  (rule: {rule})")
    except Exception as e:
        print(f"  Skipped: {department}  — {e}")

async def main():
    with open("identity/users.csv") as f:
        departments = sorted(set(row["department"] for row in csv.DictReader(f)))

    print(f"Creating {len(departments)} department groups...")
    for dept in departments:
        await create_department_group(dept)
    print("Done.")

asyncio.run(main())
