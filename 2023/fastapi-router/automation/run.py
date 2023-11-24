from db.core import DBAutomation


def run_automations(automations: list[DBAutomation]):
    for automation in automations:
        # TO DO: launch a Docker container and run the automation within it
        print(f"Running automation {automation.id}")
        print(f"Code: {automation.code}")
