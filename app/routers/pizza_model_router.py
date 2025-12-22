from fastapi import APIRouter, File, UploadFile
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv
import shutil
import os

load_dotenv()

api = os.getenv("ROBOFLOW_API_KEY")

CLIENT = InferenceHTTPClient(api_url="https://serverless.roboflow.com", api_key=api)


def get_model_result(file):
    result = CLIENT.infer(file, model_id="pizza-or-not-pizza-ovt2i/1")
    return result


router = APIRouter()


@router.post("/model/uploadfile/")
async def upload_file(uploaded_file: UploadFile = File(...)):
    top = None

    print("FILE RECEIVED:", uploaded_file.filename)
    temp_file_path = f"temp_{uploaded_file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        result = get_model_result(temp_file_path)

        if isinstance(result, dict):
            top = result.get("top", "not_found")
        else:
            top = "not_found"

    except Exception as e:
        raise e

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return top
