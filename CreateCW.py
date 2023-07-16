

from fashion_class.CapsuleWardrobe import CapsuleWardrobe
from fashion_class.FashionItem import FashionItem
from fashion_class.ImageStruct import ImageStruct
import torch

def create_cw(required_item: dict[str, list[FashionItem]], dataset, initial_items: dict[str, list[FashionItem]], eps=1e-2, max_length=4):
    cw = CapsuleWardrobe(initial_items, required_item, max_length=max_length)
    increase = eps + 1
    roop = 0
    while increase > eps:
        print(f"{roop}回目 増加分: {increase}")
        # ここ遅い。topsとかカテゴリごとに、キャッシュしてあげたほうがいい。
        increase = cw.optimize(dataset)
    return cw

def search_alternate_item(cw: CapsuleWardrobe, kind: str, index: int, dataset: ImageStruct):
    user_dislike_item = None
    alternate_item_candidate = []
    items = {
        'tops': cw.tops,
        'bottoms': cw.bottoms,
        'shoes': cw.shows
    }
    same_layer = []
    if kind == 'tops':
        alternate_item_candidate = dataset.get_tops()
        user_dislike_item = cw.tops[index]
        items['tops'] = []
        same_layer = cw.tops
    elif kind == 'bottoms':
        alternate_item_candidate = dataset.get_bottoms()
        user_dislike_item = cw.bottoms[index]
        items['bottoms'] = []
        same_layer = cw.bottoms
    elif kind == 'shoes':
        alternate_item_candidate = dataset.get_shoes()
        user_dislike_item = cw.shoes[index]
        items['shoes'] = []
        same_layer = cw.bottoms
    
    score = (0, None)
    for item in alternate_item_candidate:
        distance = torch.dist(item.img_tensor, user_dislike_item.img_tensor, p=2)
        items[kind] = item
        c = cw.calc_compatibility_increase(items)
        v = cw.calc_versatility(same_layer, item)
        # TODO: 重みづけ
        if score[0] < distance + c + v:
            score = (distance + c + v, item)
    return score[1]

