import heapq

# from ImageStruct import ImageStruct
from category import get_item_id
import torch
from fashion_class.FashionItem import FashionItem

from fashion_class.ImageStruct import ImageStruct

"""
与えられたベクトルから、画像を検索する
"""
def search_items_from_caption_embedding(word, dataset: ImageStruct, limit=10000)-> list[FashionItem]:
    heap = []
    for i in range(limit):
        if i % 100 == 0:
            progress = i // (limit // 10)
            pro_bar = "=" * progress + ' ' * (10 - progress)
            print(f"\r[{pro_bar}] {(i * 100 / limit):.1f}%", end="")
        t_img_tensor, t_img_path, _, _ = dataset.get(i)

        # 同じアイテムが入ってると寒いのではじく
        t_id = get_item_id(t_img_path)
        heap_ids = [get_item_id(i[1]) for i in heap]
        if t_id in heap_ids:
            continue
        # TODO: カテゴリに対して、意味ないものであればはじいてもいいかも。

        dist = torch.dist(word, t_img_tensor, p=2)
        heapq.heappush(heap, (-dist.item(), t_img_path, t_id))
        if len(heap) > 10:
            heapq.heappop(heap)
    fashion_items = [FashionItem(i[1]) for i in heap]
    return fashion_items
    