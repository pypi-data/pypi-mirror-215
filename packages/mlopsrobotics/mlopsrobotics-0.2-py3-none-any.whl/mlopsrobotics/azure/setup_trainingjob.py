# Author: Anouk Okkema

from azureml.core import Workspace
from azure.ai.ml import command, MLClient
from azureml.core.authentication import ServicePrincipalAuthentication
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

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

# configure job
job = command(
    code="./src",
    command="python train_object_localisation_model/evaluation_loc.py --mode cloud --",
    environment="robotic_manipulation2:18",
    compute="cluster-3",
    display_name="train-loc",
    experiment_name="train-yolo-loc-model",
)

# Submit the job
returned_job = ml_client.create_or_update(job)
