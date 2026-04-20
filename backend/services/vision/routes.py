"""
Vision Routes

Description:
API endpoints for image processing.
"""

import io
import cv2
import numpy as np

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from backend.services.vision.service import process_image
from backend.services.vision.schemas import Model

router = APIRouter(prefix="/vision", tags=["Vision"])


@router.post("/detect")
def detect(model: Model, file: UploadFile = File(...)):

    if not file.filename.lower().endswith(("jpg", "jpeg", "png")):
        raise HTTPException(status_code=415, detail="Unsupported file format")

    file_bytes = np.asarray(bytearray(file.file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    result = process_image(image, model)

    _, buffer = cv2.imencode(".jpg", result["image"])

    return StreamingResponse(io.BytesIO(buffer), media_type="image/jpeg")