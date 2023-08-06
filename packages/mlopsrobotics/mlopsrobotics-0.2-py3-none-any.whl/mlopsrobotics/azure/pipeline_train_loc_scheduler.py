# Author: Anouk Okkema

from azure.ai.ml import dsl
from azureml.core import Workspace, Experiment
from azure.ai.ml import command, MLClient
from azureml.core.authentication import ServicePrincipalAuthentication
from azure.identity import ClientSecretCredential
from PipelineScheduler import create_pipeline_schedule
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

workspace = Workspace(
    subscription_id=subscription_id,
    resource_group=resource_group,
    workspace_name=workspace_name,
    auth=service_principal,
)

experiment_list = Experiment.list(workspace=workspace)
default_experiment_name = experiment_list[0].name

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)

component_train_loc = command(
    name="loc_train_preprocess",
    display_name="Training Localisation model",
    description="Training + Preprocessing Data for loc",
    compute="cluster-3",
    inputs={
        "batch_size": Input(type="integer", description="Input batch_size"),
        "data_set": Input(
            type="uri_folder", description="Input data_path", mode="ro_mount"
        ),
        "epoch_size": Input(type="integer", description="Input epoch_size"),
        # "loc_model_path_save": Input(type="string", description="Input loc_model_path_save" ),
    },
    outputs=dict(loc_model_path_save=Output(type="uri_folder", mode="rw_mount")),
    code="./src",
    command="python train_loc.py --mode cloud --batch_size ${{inputs.batch_size}} "
    "--data_path ${{inputs.data_set}} --epoch_size ${{inputs.epoch_size}} "
    "--loc_model_path_save ${{outputs.loc_model_path_save}}",
    environment="robotic_manipulation2:18",
    experiment_name=f"{default_experiment_name}",
)
component_train_loc = ml_client.create_or_update(component_train_loc.component)


evaluate_component_loc = command(
    name="evaluate_loc",
    display_name="Loc Evaluate model",
    description="Evaluate model with data from a predefined data asset",
    inputs={
        "data_set": Input(
            type="uri_folder", description="Input data_path", mode="ro_mount"
        ),
        "loc_model_path_save": Input(type="uri_folder", description="Model URI"),
    },
    outputs=dict(squared_error_path=Output(type="uri_folder", mode="rw_mount")),
    code="./src",
    command="python train_object_localisation_model/evaluation_loc.py --mode cloud"
    " --loc_model_path_save ${{inputs.loc_model_path_save}} --data_set ${{inputs.data_set}}"
    " --squared_error_path ${{outputs.squared_error_path}}",
    environment="robotic_manipulation2:18",
    compute="cluster-3",
    experiment_name=f"{default_experiment_name}",
)
evaluate_component_loc = ml_client.create_or_update(evaluate_component_loc.component)


register_component_loc = command(
    name="register_loc",
    display_name="Loc Register model",
    description="Register model if the model meet criterium",
    inputs={
        "squared_error_path": Input(
            type="uri_folder", description="squared_error_path"
        ),
        "loc_model_path_save": Input(type="uri_folder", description="Model URI"),
    },
    outputs=dict(),
    code="./src",
    command="python train_object_localisation_model/register_loc_azure.py --mode cloud "
    "--loc_model_path_save ${{inputs.loc_model_path_save}} --squared_error_path "
    "${{inputs.squared_error_path}}",
    environment="robotic_manipulation2:18",
    compute="cluster-3",
    experiment_name=f"{default_experiment_name}",
)
register_component_loc = ml_client.create_or_update(register_component_loc.component)


@dsl.pipeline(
    name="train_localisation_pipeline",
    description="A pipeline to train an localisation model",
    compute="cluster-3",
)
def training_pipeline(batch_size: int, data_set: str, epoch_size: int) -> None:
    # Step 1: Load data
    loc_component_step = component_train_loc(
        batch_size=batch_size, data_set=data_set, epoch_size=epoch_size
    )

    evaluate_component_loc_step = evaluate_component_loc(
        loc_model_path_save=loc_component_step.outputs.loc_model_path_save,
        data_set=data_set,
    )

    register_component_loc(
        squared_error_path=evaluate_component_loc_step.outputs.squared_error_path,
        loc_model_path_save=loc_component_step.outputs.loc_model_path_save,
    )


data_path = Input(
    path="azureml://subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourcegroups/buas-y2"
    "/workspaces/MLOpsRobotics/datastores/workspaceblobstore/paths/data/object_loc_datasets",
    type="uri_folder",
    description="Input data_path",
    mode="ro_mount",
)

pipeline_instance = training_pipeline(
    batch_size=256,
    data_set=data_path,
    epoch_size=2,
    # loc_model_path_save = "./outputs/weights_Localization_XY_YAW.pt"
)

# Create pipeline schedule
pipeline_schedule = create_pipeline_schedule(
    pipeline_instance,
    "PipelineScheduleLOC",
    frequency="week",
    interval=1,
    start_time_hours=9,
    start_time_minutes=00,
    start_day="monday",
)

job_schedule = ml_client.schedules.begin_create_or_update(
    schedule=pipeline_schedule
).result()
