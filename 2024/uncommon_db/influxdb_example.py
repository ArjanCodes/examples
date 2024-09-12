from datetime import datetime

import numpy as np
from influxdb_client import InfluxDBClient, Point, Task, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Set up the InfluxDB client (replace with your token, org, and bucket details)
token = "your_token"
org = "your_org"
bucket = "example_bucket"

client = InfluxDBClient(url="http://localhost:8086", token=token)

# Example 1: Writing Time-Series Data to InfluxDB 2
write_api = client.write_api(write_options=SYNCHRONOUS)

# Simulate some data points
for i in range(100):
    point = (
        Point("cpu_load")
        .tag("host", "server01")
        .field("value", np.random.uniform(0.5, 1.5))
        .time(datetime.now(), WritePrecision.NS)
    )
    write_api.write(bucket=bucket, org=org, record=point)

# Example 2: Querying with Flux - Calculating a Moving Average
query_api = client.query_api()

flux_query = f"""
from(bucket: "{bucket}")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu_load")
  |> filter(fn: (r) => r._field == "value")
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
  |> yield(name: "mean")
"""

tables = query_api.query(flux_query)

for table in tables:
    for record in table.records:
        print(
            f"Time: {record.get_time()}, 5-Minute Moving Average: {record.get_value()}"
        )

# Example 3: Task Automation - Continuous Data Processing
# Create a task that automatically calculates and stores a rolling average every minute
task = Task(
    name="cpu_load_moving_avg",
    flux=f"""
    option task = {{
        name: "cpu_load_moving_avg",
        every: 1m
    }}
    from(bucket: "{bucket}")
      |> range(start: -1m)
      |> filter(fn: (r) => r._measurement == "cpu_load")
      |> aggregateWindow(every: 1m, fn: mean)
      |> to(bucket: "{bucket}", org: "{org}")
    """,
)

tasks_api = client.tasks_api()
tasks_api.create_task(task=task)

print("Task created to calculate and store rolling averages every minute.")
