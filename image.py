from typing import List
from pydantic.main import BaseModel
import torch
from torchvision import transforms


class ImageRequest(BaseModel):
    image: str


class ImageCategory(BaseModel):
    name: str
    precision: float


class ImageResponse(BaseModel):
    response: List[ImageCategory]


class ImageModel:
    def __init__(self):
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet152', pretrained=True)
        self.model.eval()
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def classify_image(self, image):
        input_tensor = self.preprocess(image)
        input_batch = input_tensor.unsqueeze(0)

        with torch.no_grad():
            output = self.model(input_batch)
        probabilities = torch.softmax(output[0], dim=0)

        # Read the categories
        with open("imagenet_classes.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]
        # Show top categories per image
        top5_prob, top5_catid = torch.topk(probabilities, 5)

        response = []
        for i in range(top5_prob.size(0)):
            response.append({
                "name": categories[top5_catid[i]],
                "probability": top5_prob[i].item()
            })

        return response
