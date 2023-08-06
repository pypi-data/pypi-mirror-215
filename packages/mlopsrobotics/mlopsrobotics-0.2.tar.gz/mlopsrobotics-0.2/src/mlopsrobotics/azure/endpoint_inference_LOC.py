# Author: Michael Nederhoed

# Import requried libraries
from azure.ai.ml import MLClient
from azure.identity import ClientSecretCredential
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    CodeConfiguration,
)
import datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import loguru
from utilities.logger_util import setup_logger

# Enable autologging
import mlflow

mlflow.autolog()

# Set up Logger
setup_logger(False)
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

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)

endpoint_name = "loc-endpt-" + datetime.datetime.now().strftime("%m%d%H%M%f")
logger.info(f"Endpoint name: {endpoint_name}")

# create an online endpoint
endpoint = ManagedOnlineEndpoint(
    name=endpoint_name, description="this is a sample endpoint", auth_mode="key"
)

endpoint = ml_client.online_endpoints.begin_create_or_update(endpoint).result()
logger.info(
    f"Endpoint {endpoint.name} provisioning state: {endpoint.provisioning_state}"
)

registered_model_name = "Localisation_model"
latest_model_version = 1
registered_environment_name = "inference_deploy"
latest_environment_version = 2

# picking the model to deploy. Here we use the latest version of our registered model
model = ml_client.models.get(name=registered_model_name, version=latest_model_version)
# picking the environment to deploy. Here we use the latest version of our registered environment
env = ml_client.environments.get(
    name=registered_environment_name, version=latest_environment_version
)

blue_deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name=endpoint_name,
    model=model,
    environment=env,
    code_configuration=CodeConfiguration(
        code="./src", scoring_script="score_inference_LOC.py"
    ),
    instance_type="Standard_DS4_v2",
    instance_count=1,
)


blue_deployment = ml_client.begin_create_or_update(blue_deployment).result()
ml_client.online_endpoints.get(name=endpoint_name)

endpoint = ml_client.online_endpoints.get(name=endpoint_name)
# Update the traffic distribution
endpoint.traffic["blue"] = 100
