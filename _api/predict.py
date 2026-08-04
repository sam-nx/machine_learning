import torch
import torch.nn as nn
import requests
from PIL import Image
from io import BytesIO
from torchvision import transforms, models

checkpoint = torch.load("bird_classifier.pth", map_location="cpu")
t_classes = checkpoint["classes"]
n_classes = len(t_classes)

model = models.resnet50(weights=None)
model.fc = nn.Linear(model.fc.in_features, n_classes)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def predict_from_buffer(s_buffer):
    o_image = Image.open(BytesIO(s_buffer)).convert("RGB")
    o_image_tensor = tf(o_image).unsqueeze(0)

    with torch.no_grad():
        o_output = model(o_image_tensor)
        o_probs = torch.softmax(o_output, dim=1)
        t_top_5_probs, t_top_5_idx = o_probs.topk(5, dim=1)

    return ([f"  {t_classes[n_idx]}: {o_prob.item()*100:.1f}%"
             for o_prob, n_idx in zip(t_top_5_probs[0], t_top_5_idx[0])])


if (__name__ == "__main__"):
    s_buffer = ""
    predict_from_buffer(s_buffer)
