import os
import random
import pandas as pd
from category import get_image_category
import torch

from fashion_class.FashionItem import FashionItem
NUM_ITEMS = 1270388
class ImageStruct():
    def __init__(self, annotation_file, tensor_file, init_item_length = 3000):
        # selected_indices = random.sample(range(NUM_ITEMS), init_item_length)  # init_item_length個だけランダムにインデックスを選択
        # print(selected_indices[:5])
        # self.annotations = pd.read_csv(annotation_file).iloc[selected_indices]
        # self.img_tensors = torch.load(tensor_file)[selected_indices]
        self.annotations = pd.read_csv(annotation_file)
        self.img_tensors = torch.load(tensor_file)
        self.tops: list[FashionItem] = []
        self.bottoms: list[FashionItem] = []
        self.shoes: list[FashionItem] = []
        
        for i in range(init_item_length):
            if i % 10 == 0:
                progress = '=' * (i * 100 // init_item_length) + ' ' * (100 - (i * 100 // init_item_length))
                print(f'\r【{progress}】', end='')
            _, item = self.get(i)
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
        fashion_item = FashionItem(img_path, img_tensor)
        return img_tensor, fashion_item

    def get_tops(self):
        return self.tops
    
    def get_bottoms(self):
        return self.bottoms

    def get_shoes(self):
        return self.shoes


