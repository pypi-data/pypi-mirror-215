# Author: Michael Nederhoed
# This script is to make use of our API using Azure endpoints.

# Imports
from PIL import Image
import base64
import io
import requests
import json

# Initializing Logger
import loguru
import sys

logger = loguru.logger
logger.remove()  # All configured handlers are removed
logger.add("logs/API_use.log", rotation="10 MB", level="INFO")
logger.add(
    sys.stderr,
    format="<green>{time: HH:mm:ss}</green> | <level>{level: <8}</level> "
    "| - <white>{message}</white>",
)
logger.level("SETTINGS", no=38, color="<cyan>")

logger.info("Welcome at the MLOps-robotics API")
logger.info("Input = image, output = coordinates of items")

img_path = "./data/test_images/10-b.png"
logger.log("SETTINGS", f"Chosen Image: {img_path}")
logger.info("Loading and processing image to send to API")

# Open the image file
img = Image.open(img_path)
# Create a BytesIO object
buffered = io.BytesIO()
# Save the image as jpeg to the BytesIO object
img.save(buffered, format="png")
# Get the byte value of the BytesIO object
img_byte = buffered.getvalue()
# Encode the byte to base64
img_base64 = base64.b64encode(img_byte)

img_base64_str = img_base64.decode()  # Decodeing base64
image = img_base64_str

# Keys
key_yolo = "zMtjXARBNdggpQLmW5HoG7ayG1IK6LpW"
key_loc = "DmmJ5dYKIL4TI5Sm4nEUlqnThu4wLXB7"

# Set the authentication key
headers_yolo = {"Authorization": f"Bearer {key_yolo}"}
headers_loc = {"Authorization": f"Bearer {key_loc}"}

# Set the endpoint URL
url_yolo = "https://yolo-endpt-06211330938997.westeurope.inference.ml.azure.com/score"
url_loc = "https://loc-endpt-06211602003356.westeurope.inference.ml.azure.com/score"

logger.log("SETTINGS", f"Used Key for Yolo: {key_yolo}")
logger.log("SETTINGS", f"Used Key for Loc: {key_loc}")
logger.log("SETTINGS", f"Used endpoint URL for Yolo: {url_yolo}")
logger.log("SETTINGS", f"Used endpoint URL for Loc: {url_loc}")

# Create the data payload for Yolo endpoint
data = {"image": image}
# Send the POST request and get the response
logger.info("Sending the POST to Yolo endpoint request and get the response...")
response_yolo = requests.post(url_yolo, headers=headers_yolo, data=json.dumps(data))
prediction = json.loads(response_yolo.content)  # Unpack JSON

if response_yolo.status_code == 200:
    logger.success(f"Received response: {response_yolo.status_code}")
else:
    logger.error(f"Received response: {response_yolo.status_code}")

# Create the data payload for Loc endpoint
data = {"image": image, "results": prediction}
logger.info("Sending the POST to Loc endpoint request and get the response...")
response_loc = requests.post(url_loc, headers=headers_loc, data=json.dumps(data))

if response_loc.status_code == 200:
    logger.success(f"Received response: {response_loc.status_code}")
    prediction = json.loads(response_loc.content)  # Unpack JSON
    logger.success(f"Received coordinates: {prediction}")

else:
    logger.error(f"Received response: {response_loc.status_code}")
