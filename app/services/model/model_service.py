from inference_sdk import InferenceHTTPClient
import os
from dotenv import load_dotenv 
from PIL import Image

load_dotenv()

api = os.getenv("ROBOFLOW_API_KEY")


file = Image.open("image2.jpeg")

CLIENT = InferenceHTTPClient(api_url="https://serverless.roboflow.com", api_key=api)


result = CLIENT.infer(file, model_id="pizza-or-not-pizza-ovt2i/1")
print(result)
