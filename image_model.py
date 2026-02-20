import torch
import torchvision.transforms as transforms
from torchvision import models
import numpy as np

# Load pretrained ResNet50
model = models.resnet50(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def extract_features(image):
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        features = model(image)

    features = features.numpy().flatten()

    # Normalize (CRITICAL)
    features = features / np.linalg.norm(features)

    return features
