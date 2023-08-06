# Author: Michael Nederhoed

from azureml.core import Workspace, Datastore
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core import Dataset
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = "mlopsrobotics7227516062"
KVUri = "https://mlopsrobotics7227516062.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

subscription_id = client.get_secret("subscription-id").value
resource_group = client.get_secret("resource-group").value
workspace_name = client.get_secret("workspace-name").value

ds_store_file_location = "data/.DS_store"
if os.path.isfile(ds_store_file_location):
    os.remove(ds_store_file_location)

ds_store_file_location = "data/images/.DS_store"
if os.path.isfile(ds_store_file_location):
    os.remove(ds_store_file_location)

# Log in using interactive Auth
auth = InteractiveLoginAuthentication()

# Declare workspace & datastore.
workspace = Workspace(
    subscription_id=subscription_id,
    resource_group=resource_group,
    workspace_name=workspace_name,
    auth=auth,
)

# list all datastores registered in the current workspace
datastores = workspace.datastores
for name, datastore in datastores.items():
    print(name, datastore.datastore_type)

# Create a datastore object from the existing datastore named "workspaceblobstore".
datastore = Datastore(workspace, name="workspaceblobstore")

# Upload the data to the path target_path in datastore
# datastore.upload(src_dir='../data', target_path='data', overwrite=True, show_progress=True)

# object_loc_datasets = Dataset.File.from_files(path=(datastore, 'data/object_loc_datasets'))
object_loc_weights = Dataset.File.from_files(
    path=(datastore, "data/object_loc_weights")
)

test_images = Dataset.File.from_files(path=(datastore, "data/test_images"))

Yolo_Models = Dataset.File.from_files(path=(datastore, "data/Yolo Models"))
YoloData = Dataset.File.from_files(
    path=(datastore, "data/YoloData/ConsumerGoodsTest-3")
)
Yolo_weights = Dataset.File.from_files(path=(datastore, "data/Yolo_weights"))

# Register
object_loc_weights = object_loc_weights.register(
    workspace=workspace,
    name="object_loc_weights",
    description="object_loc_weights",
    create_new_version=True,
)

test_images = test_images.register(
    workspace=workspace,
    name="test_images",
    description="test images",
    create_new_version=True,
)

# Author: Anouk Okkema
Yolo_Models = Yolo_Models.register(
    workspace=workspace,
    name="Yolo Models",
    description="Yolo models",
    create_new_version=True,
)
YoloData = YoloData.register(
    workspace=workspace,
    name="YoloData",
    description="YoloData",
    create_new_version=True,
)
Yolo_weights = Yolo_weights.register(
    workspace=workspace,
    name="Yolo_weights",
    description="Yolo_weights",
    create_new_version=True,
)

# list all datasets registered in the current workspace
datasets = workspace.datasets
for name, dataset in datasets.items():
    print(name)


# pypi-AgEIcHlwaS5vcmcCJDExMGRhMzdmLWY3YzYtNDcyZi04ZTNmLTJjODQwMjFjMTdhZAACKlszLCJkOTI5MTJiNS1iNjU3LTQxYTktOWRkMC1lZGMxYzA5Mjg2ODUiXQAABiBcL4hQU2_53nTvbkPJT35JzoQLDGZ2Gp6DQXDCrQLFIg
