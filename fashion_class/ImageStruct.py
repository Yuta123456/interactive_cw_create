import os
import pandas as pd
from category import get_image_category
import torch

from fashion_class.FashionItem import FashionItem

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
        fashion_item = FashionItem(img_path)
        return img_tensor, fashion_item
    
    def get_tops(self):
        tops: list[FashionItem] = [self.get(i)[0] for i in range(len(self)) if self.get(i)[0].get_category() == 'tops']
        return tops
    
    def get_bottoms(self):
        tops: list[FashionItem] = [self.get(i)[0] for i in range(len(self)) if self.get(i)[0].get_category() == 'bottoms']
        return tops

    def get_shoes(self):
        tops: list[FashionItem] = [self.get(i)[0] for i in range(len(self)) if self.get(i)[0].get_category() == 'shoes']
        return tops


