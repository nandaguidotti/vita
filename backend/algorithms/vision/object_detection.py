"""
Object Detection Module

Description:
Provides object detection functionality using pre-trained YOLO models.
This module is part of the algorithms layer and is independent of services or APIs.
"""
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_objects(image, model_name: str = None):
    results = model(image)

    boxes = results[0].boxes.xyxy.tolist()
    confidences = results[0].boxes.conf.tolist()
    labels = results[0].boxes.cls.tolist()

    output_image = results[0].plot()

    return output_image, boxes, labels, confidences