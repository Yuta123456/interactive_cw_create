import torch.nn as nn
import torch

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from transformers import AutoTokenizer, AutoModel
import pandas as pd
import os
import sys

sys.path.append("d:/M1/fashion")

if torch.cuda.is_available():
    device = torch.device("cuda")  # GPUデバイスを取得
else:
    device = torch.device("cpu")  # CPUデバイスを取得


class ImageEncoder(nn.Module):
    def __init__(self, embedding_size):
        super(ImageEncoder, self).__init__()
        self.resnet50 = models.resnet50(pretrained=True)
        self.fc = nn.Linear(self.resnet50.fc.out_features, embedding_size)

    def forward(self, x):
        x = self.resnet50(x)
        x = self.fc(x)
        return x


class CaptionEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModel.from_pretrained("cl-tohoku/bert-base-japanese-v2")

    def forward(self, x):
        x = self.bert(x)
        x = x.last_hidden_state

        x = x[:, 0, :]

        return x


class FashionItemEncoder(nn.Module):
    def __init__(self):
        super(FashionItemEncoder, self).__init__()
        self.image_model = ImageEncoder(768)
        self.caption_model = CaptionEncoder()
        self.fc1 = nn.Linear(768 * 2, 256)
        self.fc2 = nn.Linear(256, 64)
        self.relu = nn.ReLU()
        self.tokenizer = AutoTokenizer.from_pretrained(
            "cl-tohoku/bert-base-japanese-v2"
        )

    def load_image_dict(self, image_model_path: str):
        self.image_model.load_state_dict(torch.load(image_model_path))

    def load_caption_dict(self, caption_model_path: str):
        self.caption_model.load_state_dict(torch.load(caption_model_path))

    def forward(self, image, caption):
        image_vector = self.image_model(image)
        ids = self.tokenizer.batch_encode_plus(
            caption,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=256,
            add_special_tokens=True,
        ).input_ids
        ids = ids.to(device)
        caption_vector = self.caption_model(ids)
        concat_vector = torch.cat((image_vector, caption_vector), dim=1)
        concat_vector = self.relu(concat_vector)
        y = self.fc1(concat_vector)
        y = self.relu(y)
        y = self.fc2(y)
        return y


def get_model():
    compatibility_model_name = (
        "D:/M1/fashion/learning/model/model_compatibility_2023-11-11.pth"
    )
    versatility_model_name = (
        "D:/M1/fashion/learning/model/model_versatility_2023-12-04.pth"
    )
    compatibility_model = FashionItemEncoder().to(device)
    compatibility_model.load_state_dict(torch.load(compatibility_model_name))
    compatibility_model.eval()
    versatility_model = FashionItemEncoder().to(device)
    versatility_model.load_state_dict(torch.load(versatility_model_name))
    versatility_model.eval()

    return compatibility_model, versatility_model
