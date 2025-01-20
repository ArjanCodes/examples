import os

from convex import ConvexClient
from dotenv import load_dotenv

load_dotenv("../.env.local")
CONVEX_URL = os.getenv("VITE_CONVEX_URL")
print(CONVEX_URL)
client = ConvexClient(CONVEX_URL)

client.mutation("metrics:insert", {"name": "monthly_customers", "value": 500})

# print(client.query("tasks:get"))

# for tasks in client.subscribe("tasks:get"):
#     print(tasks)
#     # this loop lasts forever, ctrl-c to exit it
