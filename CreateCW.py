from fashion_class.FashionItem import FashionItem
from fashion_class.CapsuleWardrobeClass import CapsuleWardrobe
from fashion_class.ImageStruct import ImageStruct
import torch
import copy
def create_cw(required_item: dict[str, list[FashionItem]], dataset, initial_items: dict[str, list[FashionItem]]=None, eps=1e-2, max_length=4):
    cw = CapsuleWardrobe(initial_items, required_item, max_length=max_length)
    increase = eps + 1
    roop = 0
    pre_cw = copy.deepcopy(cw)
    while increase > eps:
        # ここ遅い。topsとかカテゴリごとに、キャッシュしてあげたほうがいい。
        increase = cw.optimize(dataset)
        pre_cw = copy.deepcopy(cw)
        print(f"{roop}回目 増加分: {increase}")
        if increase < 0:
            print('ロールバックします')
            cw = pre_cw
    return cw

def search_alternate_item(cw: CapsuleWardrobe, kind: str, index: int, dataset: ImageStruct):
    user_dislike_item = None
    alternate_item_candidate = []
    items = {
        'tops': cw.get_tops(),
        'bottoms': cw.get_bottoms(),
        'shoes': cw.get_shoes()
    }
    same_layer = []
    if kind == 'tops':
        alternate_item_candidate = dataset.get_tops()
        user_dislike_item = cw.get_tops()[index]
        items['tops'] = []
        same_layer = cw.get_tops()
    elif kind == 'bottoms':
        alternate_item_candidate = dataset.get_bottoms()
        user_dislike_item = cw.get_bottoms()[index]
        items['bottoms'] = []
        same_layer = cw.get_bottoms()
    elif kind == 'shoes':
        alternate_item_candidate = dataset.get_shoes()
        user_dislike_item = cw.get_shoes()[index]
        items['shoes'] = []
        same_layer = cw.get_shoes()

    score = (0, None)
    for item in alternate_item_candidate:
        distance = torch.dist(item.img_tensor, user_dislike_item.img_tensor, p=2)
        items[kind] = [item]
        c = cw.calc_compatibility_increase(items)
        v = cw.calc_versatility_increase(same_layer, item)
        # TODO: 重みづけ
        if score[0] < distance + c + v:
            score = (distance + c + v, item)
    return score[1]

def change_item_recommandation(cw: CapsuleWardrobe):
    # 全てのアイテムが一つ多い
    # 一番最後に推薦するアイテムが入っている
    initial_items = {
        'tops': cw.get_tops(),
        'bottoms':cw.get_bottoms(),
        'shoes':cw.get_shoes()
    }
    remove_item_indexes = {
        'tops':None, 
        'bottoms': None,
        'shoes': None
    }

    for k, category_list in zip(['tops', 'bottoms', 'shoes'], [cw.tops, cw.bottoms, cw.shoes]):
        worst_item_score = (10e10, None)
        for i, _ in enumerate(category_list):
            copy_items = initial_items.copy()
            copy_items[k].pop(i)
            cw = CapsuleWardrobe(initial_items=copy_items)
            cw_score = cw.calc_self_cw_compatibility() + cw.calc_self_cw_versatility()
            if worst_item_score[0] > cw_score:
                worst_item_score = (cw_score, i)
        remove_item_indexes[k] = worst_item_score[1]
    
    return remove_item_indexes