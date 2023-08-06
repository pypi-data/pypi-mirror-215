from azureml.core import Model
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
import argparse
import os
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


class AzureMLModelRegister:
    def __init__(
        self,
        model: str,
        model_name: str,
        evaluation_outputs_folder: str,
        threshold: float = 0.8,
    ):
        """
        Initializes an AzureMLModelRegister object.

        Args:
            model (str): The path to the model file.
            model_name (str): The name to assign to the registered model.
            evaluation_outputs_folder (str): The folder path where evaluation outputs are stored.
            threshold (float, optional): The threshold value for model accuracy. Defaults to 0.8.

        Author: Anouk Okkema
        """
        logger.info(f"Registering model if accuracy is above {threshold}.")
        logger.info(f"Model path: {model}")
        logger.info(f"Accuracy folder: {evaluation_outputs_folder}")

        self.model_name = model_name
        self.model = model
        self.evaluation_outputs_folder = evaluation_outputs_folder
        self.threshold = threshold
        self.mAP50_95 = None

    def MAP_threshold(self) -> None:
        """
        Loads the accuracy metric (mAP50-95(B)) from the evaluation outputs file.

        Author: Anouk Okkema
        """
        # Get the evaluation_outputs_file
        evaluation_outputs_file = os.path.join(
            self.evaluation_outputs_folder, "output_results.txt"
        )
        # Load accuracy from file
        with open(evaluation_outputs_file, "r") as f:
            for line in f:
                if line.startswith("metrics/mAP50-95(B)"):
                    self.mAP50_95 = float(line.split(":")[1].strip())
                    break

        logger.info(f"mAP50-95(B): {self.mAP50_95}")

    def registermodel(self) -> None:
        """
        Registers the model if its accuracy is above the threshold.

        Author: Anouk Okkema
        """
        # Only register model if accuracy is above threshold
        if self.mAP50_95 is not None and self.mAP50_95 > self.threshold:
            logger.info("Model accuracy is above threshold, registering model.")

            registered_model = Model.register(
                model_path=self.model, model_name=self.model_name, workspace=workspace
            )

            logger.info("Model registered:", registered_model.name)

        else:
            logger.info("Model accuracy is not above threshold, not registering model.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        help="Image size for training (default: 640)",
        default="data/Yolo_weights/best.pt",
        required=False,
    )
    parser.add_argument(
        "--model_name",
        type=str,
        help="Batch size for training (default: 16)",
        default="yolo_trainedmodel",
        required=False,
    )
    parser.add_argument(
        "--evaluation_outputs",
        type=str,
        help="Directory of evaluation outputs",
        default="outputs/testresults/",
        required=False,
    )
    args = parser.parse_args()

    register = AzureMLModelRegister(
        model=args.model,
        model_name=args.model_name,
        evaluation_outputs_folder=args.evaluation_outputs,
    )
    # Call the retrieve_datasetpath method
    register.MAP_threshold()
    register.registermodel()
