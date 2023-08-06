# Author: Elisabeth Engering

# Import required libraries
from azure.ai.ml import dsl
from azureml.core import Workspace
from azure.ai.ml import command, MLClient
from azureml.core.authentication import ServicePrincipalAuthentication
from azure.identity import ClientSecretCredential
from azure.ai.ml import Input, Output
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

# Declare workspace & datastore
workspace = Workspace(
    subscription_id=subscription_id,
    resource_group=resource_group,
    workspace_name=workspace_name,
    auth=service_principal,
)

# Get a handle to the workspace
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)

# Create component of inference.py
component_inference = command(
    name="Inference",
    display_name="Inference",
    description="Performs inference using YOLO and a localization model on an image.",
    compute="cluster-3",
    inputs={
        "user_input": Input(
            type="string", description="User choice to change default settings"
        ),
        "model_path": Input(
            type="uri_folder",
            description="Path to the YOLO model weight file",
            mode="ro_mount",
        ),
        "image_path": Input(type="uri_folder", description="Path to the image file"),
        "loc_model_path": Input(
            type="uri_folder", description="Path to the localisation model weight file"
        ),
    },
    outputs={
        "classes": Output(mode="rw_mount"),
        "output": Output(mode="rw_mount"),
        "output2": Output(mode="rw_mount"),
        "output3": Output(mode="rw_mount"),
    },
    code="./src",
    command="python inference.py --mode cloud --user_input ${{inputs.user_input}} "
    "--model_path ${{inputs.model_path}} --image_path ${{inputs.image_path}} "
    "--loc_model_path ${{inputs.loc_model_path}}",
    environment="robotic_manipulation2:18",
)


# Build pipeline
@dsl.pipeline(
    name="inference_pipeline",
    description="A pipeline that uses YOLO and a localization model on an image",
    compute="cluster-3",
)
def inference_pipeline(
    user_input: str, model_path: str, image_path: str, loc_model_path: str
) -> None:
    component_inference(
        user_input=user_input,
        model_path=model_path,
        image_path=image_path,
        loc_model_path=loc_model_path,
    )


model_path_input = Input(
    path="azureml://subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourcegroups/buas-y2/"
    "workspaces/MLOpsRobotics/datastores/workspaceblobstore/paths/data/Yolo_weights",
    type="uri_folder",
    description="Input model_path",
    mode="ro_mount",
)


image_path_input = Input(
    path="azureml://subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourcegroups/"
    "buas-y2/workspaces/MLOpsRobotics/datastores/workspaceblobstore"
    "/paths/data/test_images/10-b.png",
    type="uri_file",
    description="Input image_path",
    mode="ro_mount",
)

loc_model_path_input = Input(
    path="azureml://subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourcegroups/buas-y2"
    "/workspaces/MLOpsRobotics/datastores/workspaceblobstore/paths/data/object_loc_weights",
    type="uri_folder",
    description="Input loc_model_path",
    mode="ro_mount",
)

# Create instance of a command
pipeline_instance = inference_pipeline(
    user_input="no",
    model_path=model_path_input,
    image_path=image_path_input,
    loc_model_path=loc_model_path_input,
)

pipeline_run = ml_client.jobs.create_or_update(pipeline_instance)
