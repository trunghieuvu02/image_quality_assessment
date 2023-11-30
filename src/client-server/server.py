import sys

sys.path.append("..")
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from PIL import Image
from io import BytesIO
import numpy as np
from blur_detector.blur_detector import detect_blur_spot
import cv2
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()
# Increase the maximum request body size
app.max_request_size = 5 * 1024 * 1024  # For example, set to 5 MB

class Data(BaseModel):
    name: str
@app.post("/create/")
async def create(data: Data):
    return {"data": data}

@app.get("/test/{item_id}/")
async def say_hello(item_id: str, query: int = 1):
    return f"Hello, Hieu! This is {item_id}"


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = file.file.read()
    # Convert the binary contents to an Image object using PIL
    image = Image.open(BytesIO(contents))

    # Convert the PIL Image to a NumPy array
    numpy_image = np.array(image)

    blur_image, blur_text, blurry_score = detect_blur_spot(numpy_image, 100)

    # blur_image.save("uploaded_image.jpg")
    cv2.imwrite("uploaded_image.jpg", blur_image)

    return {
        "message": f"Successfully uploaded {file.filename}, image quality: {blur_text}, blurry score: {blurry_score}"}
