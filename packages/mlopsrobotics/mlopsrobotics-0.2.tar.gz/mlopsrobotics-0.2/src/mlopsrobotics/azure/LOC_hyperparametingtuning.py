# Author: Anouk Okkema

from azure.ai.ml.sweep import Uniform
from azureml.core import Workspace
from azure.ai.ml import command, MLClient
from azureml.core.authentication import ServicePrincipalAuthentication
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml import Input

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

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)

data_path = Input(
    path="azureml://subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourcegroups/buas-y2/"
    "workspaces/MLOpsRobotics/datastores/workspaceblobstore/paths/data/object_loc_datasets",
    type="uri_folder",
    description="Input data_path",
    mode="ro_mount",
)

# configure job
job = command(
    inputs=dict(
        data_path=data_path,
        batch_size=64,
        epoch_size=5,
        loc_model_path_save="data/object_loc_weights/New_weights_loc.pt",
    ),
    code="./src",
    command="python train_loc.py  --batch_size ${{inputs.batch_size}}"
    " --epoch_size ${{inputs.epoch_size}} --data_path ${{inputs.data_path}}",
    environment="robotic_manipulation2:18",
    compute="cluster-gpu",
    display_name="hyperparameter-loc",
    experiment_name="hyperparemeting",
)

job_for_sweep = job(
    batch_size=Uniform(min_value=16, max_value=32),
    epoch_size=Uniform(min_value=5, max_value=10),
)

sweep_job = job_for_sweep.sweep(
    compute="cluster-gpu",
    sampling_algorithm="random",
    primary_metric="best_val_acc",
    goal="Maximize",
    max_total_trials=2,
    max_concurrent_trials=4,
)

returned_sweep_job = ml_client.create_or_update(sweep_job)

# stream the output and wait until the job is finished
ml_client.jobs.stream(returned_sweep_job.name)
