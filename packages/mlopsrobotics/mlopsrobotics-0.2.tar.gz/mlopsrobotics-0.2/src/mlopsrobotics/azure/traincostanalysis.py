# Author: Anouk Okkema

from azureml.core.authentication import ServicePrincipalAuthentication
from azure.identity import ClientSecretCredential
from azureml.core import Workspace, Experiment
from datetime import datetime
import pandas as pd
from tabulate import tabulate
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from utilities.logger_util import setup_logger
import loguru

# Set up Logger
setup_logger(True)
logger = loguru.logger

keyVaultName = "mlopsrobotics7227516062"
KVUri = "https://mlopsrobotics7227516062.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

tenant_id = client.get_secret("tenant-id").value
client_id = client.get_secret("client-id").value
client_secret = client.get_secret("client-secret").value
subscription_id = client.get_secret("subscription-id").value
resource_group = client.get_secret("resource-group").value
workspace_name = client.get_secret("workspace-name").value

service_principal = ServicePrincipalAuthentication(
    tenant_id=tenant_id,
    service_principal_id=client_id,
    service_principal_password=client_secret,
)

workspace = Workspace(
    subscription_id=subscription_id,
    resource_group=resource_group,
    workspace_name=workspace_name,
    auth=service_principal,
)

experiment_list = Experiment.list(workspace=workspace)
default_experiment_name = experiment_list[0].name

experiment = Experiment(workspace, default_experiment_name)

# Retrieve and analyze experiment runs
runs = experiment.get_runs()

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

total_cost = 0

# Create a list to store the run information
run_info_list = []

# Iterate through runs
for run in runs:
    run_details = run.get_details()

    if run_details["status"] == "Completed":
        # Extract relevant information such as compute target, start time, end time, etc.
        compute_name = run_details["properties"]["azureml.defaultComputeName"]
        compute_target = workspace.compute_targets[compute_name]
        vm_size = compute_target.vm_size

        # Start time
        starttime = run_details["startTimeUtc"]
        start_time = datetime.strptime(starttime, "%Y-%m-%dT%H:%M:%S.%fZ")
        vm_size = compute_target.vm_size

        # End time
        endtime = run_details["endTimeUtc"]
        end_time = datetime.strptime(endtime, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Calculate run duration
        duration = (end_time - start_time).total_seconds() / 3600  # in hours

        if compute_name == "cluster-gpu":
            compute_cost_per_hour = 1.17
        elif compute_name == "cluster-2":
            compute_cost_per_hour = 0.27
        elif compute_name == "cluster-3":
            compute_cost_per_hour = 0.27
        else:
            compute_cost_per_hour = 0

        # Calculate training cost for the run based on cost factors and duration
        run_cost = duration * compute_cost_per_hour

        # Get the display name of the run
        run_id = run_details["runId"]
        if run_id.startswith("Pipeline"):
            display_name = run_details["properties"]["azureml.genericTriggerName"]
        else:
            display_name = run_details["runDefinition"]["DisplayName"]

        # Store the run information in a dictionary
        run_info = {
            "Display Name": display_name,
            "Compute Target": compute_name,
            "Virtual Machine Size": vm_size,
            "Start Time": start_time,
            "End Time": end_time,
            "Duration (hours)": duration,
            "Training Cost ($)": run_cost,
        }

        # Add the run information to the list
        run_info_list.append(run_info)

# Create a DataFrame from the run information list
run_cost = pd.DataFrame(run_info_list)

# Calculate the total training cost
total_cost = run_cost["Training Cost"].sum()

# Calculate training cost per display name
cost_per_displayname = (
    run_cost.groupby("Display Name")["Training Cost"].sum().reset_index()
)

# Create a new row for total training cost
total_row = pd.DataFrame({"Display Name": ["Total"], "Training Cost": [total_cost]})

# Concatenate the DataFrames
total_cost_df = pd.concat([cost_per_displayname, total_row], ignore_index=True)

# Format the DataFrame as a table
rowtable = tabulate(run_cost, headers="keys", tablefmt="github")

table = tabulate(total_cost_df, headers="keys", tablefmt="github")

# Introduction to the training cost analysis
intro_text = "# Training Cost Analysis\n\n"
intro_text += "This document provides an analysis of the training costs for different runs in the "
"experiment.\n"
intro_text += "The training costs are calculated based on the duration of each run and"
" the associated compute targets.\n\n"
intro_text += (
    "The specific cost rates used for different compute targets are as follows:\n"
)
intro_text += "- `cluster-gpu`: $1.17 per hour\n"
intro_text += "- `cluster-2`: $0.27 per hour\n"
intro_text += "- `cluster-3`: $0.27 per hour\n\n"

# Write the table to the readme.md file
with open("docs/train_cost_analysis.md", "w") as f:
    f.write(intro_text)
    f.write("\n\n## Run Cost Breakdown\n")
    f.write(
        "The following table provides a breakdown of the training costs per run:\n\n"
    )
    f.write(rowtable)
    f.write("\n\n")

    f.write("## Total Training Cost\n")
    f.write(
        "The total training cost across all runs is calculated as shown in the following table:\n"
    )
    f.write(table)

logger.info("Results written to train_cost_analysis.md file.")
