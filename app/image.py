from typing import List

from pydantic.main import BaseModel


class ImageRequest(BaseModel):
    image: str


class ImageCategory(BaseModel):
    name: str
    precision: float


class ImageResponse(BaseModel):
    response: List[ImageCategory]


class ImageModel:
    def __init__(self):
        self.model = None
        pass

    def classify_image(self, image):
        return [
            {
                "name": "murcielago",
                "precision": 20.0
            },
            {
                "name": "Otro",
                "precision": 30.0
            },
        ]