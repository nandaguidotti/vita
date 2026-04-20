"""
Vision Schemas

Description:
Defines input/output contracts and enumerations for vision services.
"""

from enum import Enum


class Model(str, Enum):
    yolov3tiny = "yolov3-tiny"
    yolov3 = "yolov3"