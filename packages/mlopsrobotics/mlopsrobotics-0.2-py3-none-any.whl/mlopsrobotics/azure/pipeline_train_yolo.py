# Author: Anouk Okkema

from azure.ai.ml.sweep import Uniform
from azureml.core import Workspace, Experiment
from azure.ai.ml import command, MLClient
from azure.ai.ml import dsl
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

# Definieer de commando-component voor training
# Definieer de commando-component voor training
train_component = command(
    name="hyperparameter_tuning",
    display_name="Sweep Job",
    description="Train YOLO model with data from a predefined data asset",
    compute="cluster-gpu",
    inputs={
        "data_path": Input(
            type="uri_folder", description="Input data path", mode="ro_mount"
        ),
        "img_size": Input(type="integer", description="Image size for training"),
        "batch_size": Input(type="integer", description="Batch size for training"),
        "epochs": Input(type="integer", description="Epochs for training"),
        "model_weight": Input(
            type="uri_file",
            description="The weight model file for the model used",
            mode="ro_mount",
        ),
        "mode": Input(type="string", description="cloud or local"),
        "project": Input(type="string", description="the experiment name"),
    },
    outputs={"model": Output(type="uri_folder", mode="rw_mount")},
    code="./src",
    command="python -m train_computer_vision_model.train_YoloV5 --img_size ${{inputs.img_size}}"
    " --batch_size ${{inputs.batch_size}} --epochs ${{inputs.epochs}}"
    " --model_weight ${{inputs.model_weight}} --data_path ${{inputs.data_path}}"
    " --mode ${{inputs.mode}} --project ${{inputs.project}} --model_path ${{outputs.model}}",
    environment="robotic_manipulation2:18",
)

train_component = ml_client.create_or_update(train_component.component)

evaluate_component = command(
    name="evaluating_model",
    display_name="Evaluate Job",
    description="Evaluate Trained YOLO model with data from a predefined data asset",
    compute="cluster-gpu",
    inputs={
        "model": Input(type="uri_folder", description="Model URI"),
        "test_dataset_dir": Input(
            type="uri_folder", description="Input data path", mode="ro_mount"
        ),
        "project": Input(type="string", description="the experiment name"),
        "mode": Input(type="string", description="cloud or local"),
    },
    outputs={"evaluation_outputs": Output(type="uri_folder", mode="rw_mount")},
    code="./src",
    command="python -m train_computer_vision_model.evaluate_script"
    " --model_path ${{inputs.model}} --test_dataset_dir ${{inputs.test_dataset_dir}}"
    " --project ${{inputs.project}} --mode ${{inputs.mode}}"
    " --output_dir ${{outputs.evaluation_outputs}}",
    environment="robotic_manipulation2:18",
)

evaluate_component = ml_client.create_or_update(evaluate_component.component)

# Definieer de commando-component voor training
register_component = command(
    name="register_model",
    display_name="Register Job",
    description="Register YOLO Model",
    compute="cluster-gpu",
    inputs={
        "model": Input(type="uri_folder", description="Model URI"),
        "model_name": Input(type="string", description="Model Name"),
        "evaluation_outputs": Input(
            type="uri_folder", description="Model URI", mode="ro_mount"
        ),
    },
    code="./src",
    command="python -m MLOpsRobotics.azure.register_model --model ${{inputs.model}}"
    " --model_name ${{inputs.model_name}} --evaluation_outputs ${{inputs.evaluation_outputs}}",
    environment="robotic_manipulation2:18",
)

register_component = ml_client.create_or_update(register_component.component)


@dsl.pipeline(
    name="hyper_yolo_pipeline",
    description="A pipeline to train an yolo model",
    compute="cluster-gpu",
    environment="robotic_manipulation2:18",
)
def training_pipeline(model_weight: str, data_path: str) -> None:
    train_step = train_component(
        img_size=Uniform(min_value=200, max_value=240),
        batch_size=Uniform(min_value=16, max_value=32),
        epochs=Uniform(min_value=1, max_value=2),
        model_weight=YOLOmodel,
        data_path=dataset,
        mode="cloud",
        project=default_experiment_name,
    )

    sweep_step = train_step.sweep(
        compute="cluster-gpu",
        sampling_algorithm="random",
        primary_metric="metrics/mAP50-95B",
        goal="Maximize",
        max_total_trials=2,
        max_concurrent_trials=3,
    )

    evaluate_step = evaluate_component(
        model=sweep_step.outputs.model,
        test_dataset_dir=dataset,
        project=default_experiment_name,
        mode="cloud",
    )

    register_component(
        model=sweep_step.outputs.model,
        model_name="YoloV5Model",
        evaluation_outputs=evaluate_step.outputs.evaluation_outputs,
    )


dataset = Input(
    path="azureml://subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourcegroups/buas-y2"
    "/workspaces/MLOpsRobotics/datastores/workspaceblobstore/paths/data"
    "/YoloData/ConsumerGoodsTest-3",
    type="uri_folder",
    description="Input data_path",
    mode="ro_mount",
)


YOLOmodel = Input(
    path="azureml://subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourcegroups/buas-y2/"
    "workspaces/MLOpsRobotics/datastores/workspaceblobstore/paths/data/Yolo Models/yolov5s6u.pt",
    type="uri_file",
    description="Input model",
    mode="ro_mount",
)

# Maak een instantie van de pipeline
pipeline_instance = training_pipeline(
    model_weight=YOLOmodel,
    data_path=dataset,
)

pipeline_run = ml_client.jobs.create_or_update(pipeline_instance)

ml_client.jobs.stream(pipeline_run.name)
