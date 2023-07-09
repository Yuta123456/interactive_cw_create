import os
import pandas as pd
import numpy as np
from PIL import Image
from category import get_image_category
import torch

class ImageStruct():
    def __init__(self, annotation_file, tensor_file):
        self.annotations = pd.read_csv(annotation_file)
        self.img_tensors = torch.load(tensor_file)
    
    def __len__(self):
        return len(self.annotations)

    def get(self, idx):
        # D:/M1/fashion/IQON/IQON3000\1000092\3933191/11258659_m.jpg, 2016　Autumn&Winter　e-MOOK掲載商品 宮田聡子さん NVY着用トレンドのラップデザインを、ミドル丈でレディにクラスアップさせたスカート。サイドフリンジが存在感のあるアクセントに。シンプルなトップスを合わせ、今季らしい着こなしを楽しんで。
        img_tensor = self.img_tensors[idx]
        img_path = self.annotations.iloc[idx, 0]
        caption = self.annotations.iloc[idx, 1]
        category = get_image_category(img_path)
        return img_tensor, img_path, category, caption
    

