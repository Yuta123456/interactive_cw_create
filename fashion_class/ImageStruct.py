import os
import random
import pandas as pd
from category import get_image_category
import torch

from fashion_class.FashionItem import FashionItem

class ImageStruct():
    def __init__(self, annotation_file, tensor_file, init_item_length = 3000):
        self.annotations = pd.read_csv(annotation_file)
        self.img_tensors = torch.load(tensor_file)
        self.tops = []
        self.bottoms = []
        self.shoes = []
        
        for i in range(init_item_length):
            if i % 10 == 0:
                progress = '=' * (i * 100 // init_item_length) + ' ' * (100 - (i * 100 // init_item_length))
                print(f'\r【{progress}】', end='')
            item = self.get(random.randint(0, len(self)))[1]
            if item.get_category() == "tops":
                self.tops.append(item)
            if item.get_category() == "bottoms":
                self.bottoms.append(item)
            if item.get_category() == "shoes":
                self.shoes.append(item)
        
    def __len__(self):
        return len(self.annotations)

    def get(self, idx):
        # D:/M1/fashion/IQON/IQON3000\1000092\3933191/11258659_m.jpg, 2016　Autumn&Winter　e-MOOK掲載商品 宮田聡子さん NVY着用トレンドのラップデザインを、ミドル丈でレディにクラスアップさせたスカート。サイドフリンジが存在感のあるアクセントに。シンプルなトップスを合わせ、今季らしい着こなしを楽しんで。
        img_tensor = self.img_tensors[idx]
        img_path = self.annotations.iloc[idx, 0]
        fashion_item = FashionItem(img_path)
        return img_tensor, fashion_item

    def get_tops(self):
        tops: list[FashionItem] = [self.get(i)[1] for i in range(len(self)) if self.get(i)[1].get_category() == 'tops']
        return tops[:100]
    
    def get_bottoms(self):
        bottoms: list[FashionItem] = [self.get(i)[1] for i in range(len(self)) if self.get(i)[1].get_category() == 'bottoms']
        return bottoms[:100]

    def get_shoes(self):
        shoes: list[FashionItem] = [self.get(i)[1] for i in range(len(self)) if self.get(i)[1].get_category() == 'shoes']
        return shoes[:100]


