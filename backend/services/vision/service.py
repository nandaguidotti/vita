"""
Vision Service Layer

Description:
Handles business logic for vision processing.
Acts as an intermediary between API routes and algorithms.
"""

from backend.algorithms.vision.object_detection import detect_objects


def process_image(image, model: str):
    """
    Process an image using the selected detection model.

    Args:
        image: Input image (OpenCV format)
        model (str): Model name

    Returns:
        dict: Processed image and detection metadata
    """
    output_image, bbox, label, conf = detect_objects(image)

    return {
        "image": output_image,
        "detections": [
            {
                "label": l,
                "confidence": float(c),
                "bbox": b
            }
            for l, c, b in zip(label, conf, bbox)
        ]
    }