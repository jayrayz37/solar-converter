from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
import tifffile
import numpy as np
from io import BytesIO

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    raw = await file.read()

    with tifffile.TiffFile(BytesIO(raw)) as tif:
        arr = tif.asarray()

    arr = np.squeeze(arr)
    arr = arr.astype("float32")
    arr = (arr - arr.min()) / (arr.max() - arr.min())
    arr = (arr * 255).astype("uint8")

    img = Image.fromarray(arr)
    img.thumbnail((500, 350))

    output = BytesIO()
    img.save(output, format="PNG")

    return Response(content=output.getvalue(), media_type="image/png")