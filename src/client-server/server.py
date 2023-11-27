from fastapi import FastAPI, File, UploadFile

app = FastAPI()
# Increase the maximum request body size
app.max_request_size = 5 * 1024 * 1024  # For example, set to 5 MB


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
