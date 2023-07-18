import heapq

# from ImageStruct import ImageStruct
from category import get_item_id
import torch
from fashion_class.FashionItem import FashionItem

from fashion_class.ImageStruct import ImageStruct

"""
与えられたベクトルから、画像を検索する
"""
def search_items_from_caption_embedding(word, dataset: list[FashionItem],  limit=10000)-> list[FashionItem]:
    heap = []
    for i in range(limit):
        if i % 100 == 0:
            progress = i // (limit // 10)
            pro_bar = "=" * progress + ' ' * (10 - progress)
            print(f"\r[{pro_bar}] {(i * 100 / limit):.1f}%", end="")
        fashion_item = dataset[i]
        t_img_tensor = fashion_item.img_tensor

        # 同じアイテムが入ってると寒いのではじく
        heap_ids = [i[1].item_id for i in heap]
        if fashion_item.item_id in heap_ids:
            continue

        dist = torch.dist(word, t_img_tensor, p=2)
        heapq.heappush(heap, (-dist.item(), fashion_item))
        if len(heap) > 10:
            heapq.heappop(heap)
    fashion_items: list[FashionItem] = [i[1] for i in heap]
    return fashion_items
    