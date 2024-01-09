import os
import subprocess
from pathlib import Path
import json
import requests

from pulumi import automation as auto
from ..core import DBAutomation


STACK_NAME = "dev_auto"


def prepare_virtual_environment(work_dir: str):
    print("preparing virtual environment...")
    subprocess.run(
        ["python3", "-m", "venv", "venv"], check=True, cwd=work_dir, capture_output=True
    )
    subprocess.run(
        [
            os.path.join("venv", "bin", "python3"),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ],
        check=True,
        cwd=work_dir,
        capture_output=True,
    )
    subprocess.run(
        [os.path.join("venv", "bin", "pip"), "install", "-r", "requirements.txt"],
        check=True,
        cwd=work_dir,
        capture_output=True,
    )
    print("virtual environment is ready!")


def run_automations(automations: list[DBAutomation]):
    for automation in automations:
        print(f"Running automation {automation.id}")
        print(f"Code: {automation.code}")

        # define the working directory as the code_runner directory
        work_dir = os.path.join(Path(__file__).parent, "../../../code_runner")

        prepare_virtual_environment(work_dir)

        # Create our stack using a local program in the ./code_runner directory
        stack = auto.create_or_select_stack(stack_name=STACK_NAME, work_dir=work_dir)
        print("successfully initialized stack")

        print("updating stack...")
        up_res = stack.up(on_output=print)
        print(
            f"update summary: \n{json.dumps(up_res.summary.resource_changes, indent=4)}"
        )
        function_url = up_res.outputs["fxn_url"].value

        print(f"Function url: {up_res.outputs['fxn_url'].value}")

        # Invoke the function
        print("invoking function...")
        response = requests.post(
            function_url, json={"code": automation.code}, timeout=60
        )
        print(f"function response: {response.text}")

        # Destroy the stack, returning the final state of the stack.
        print("destroying stack...")
        stack.destroy(on_output=print)
