from inference_sdk import InferenceHTTPClient
from PIL import Image


file = Image.open("image.png")

CLIENT = InferenceHTTPClient(api_url="https://serverless.roboflow.com", api_key="")


result = CLIENT.infer(file, model_id="pizza-or-not-pizza-ovt2i/1")
print(result)
