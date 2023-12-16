from fashion_class.FashionItem import FashionItem
from fashion_class.CapsuleWardrobeClass import LAYER, CapsuleWardrobe
from fashion_class.ImageStruct import ImageStruct
import torch
import copy
from getModel import get_model

if torch.cuda.is_available():
    device = torch.device("cuda")  # GPUデバイスを取得
else:
    device = torch.device("cpu")  # CPUデバイスを取得

compatibility_model, versatility_model = get_model()

c_model, v_model = get_model()


def create_cw(
    required_item: dict[str, list[FashionItem]],
    dataset,
    initial_items: dict[str, list[FashionItem]] = None,
    eps=1e-3,
    max_length=4,
):
    cw = CapsuleWardrobe(initial_items, required_item, max_length=max_length)
    increase = eps + 1
    roop = 0
    pre_cw = copy.deepcopy(cw)
    while increase > eps:
        # ここ遅い。topsとかカテゴリごとに、キャッシュしてあげたほうがいい。
        increase = cw.optimize(dataset)
        pre_cw = copy.deepcopy(cw)
        # print(f"{roop}回目 増加分: {increase}")
        if increase < 0:
            # print('ロールバックします')
            cw = pre_cw
    # print(f'cwのスコア: {cw.get_score()}')
    return cw


def search_alternate_item(
    cw: CapsuleWardrobe,
    kind: str,
    index: int,
    dataset: ImageStruct,
    user_like_items,
    user_dislike_items,
):
    user_dislike_item = None
    alternate_item_candidate = []
    items = {
        "tops": cw.get_tops(),
        "bottoms": cw.get_bottoms(),
        "shoes": cw.get_shoes(),
    }
    same_layer = []
    if kind == "tops":
        alternate_item_candidate = dataset.get_tops()
        user_dislike_item = cw.get_tops()[index]
        items["tops"] = []
        same_layer = cw.get_tops()
    elif kind == "bottoms":
        alternate_item_candidate = dataset.get_bottoms()
        user_dislike_item = cw.get_bottoms()[index]
        items["bottoms"] = []
        same_layer = cw.get_bottoms()
    elif kind == "shoes":
        alternate_item_candidate = dataset.get_shoes()
        user_dislike_item = cw.get_shoes()[index]
        items["shoes"] = []
        same_layer = cw.get_shoes()

    score = (0, None)
    distance_compatibility = calc_candidate_items_vector_distance(
        user_like_items, alternate_item_candidate, c_model
    )
    distance_versatility = calc_candidate_items_vector_distance(
        user_dislike_items, alternate_item_candidate, v_model
    )
    item_ids = [i.item_id for i in same_layer]
    for i, item in enumerate(alternate_item_candidate):
        if item.item_id in item_ids:
            continue
        items[kind] = [item]

        # 既存のcwへの適応度のスコア
        c = cw.calc_compatibility_increase(items)
        v = cw.calc_versatility_increase(same_layer, item)

        # ユーザの好みのスコア
        p_c = distance_compatibility[i]
        p_v = distance_versatility[i]
        # TODO: 重みづけ
        new_score = p_c + p_v + c + v
        if score[0] < new_score:
            score = (new_score, item)
    return score[1]


def calc_candidate_items_vector_distance(
    user_items, candidate_items, model, closest=True
):
    # # alternate_itemが、compatibilityと、versatilityで優れているか？
    user_items_vector = []
    for item in user_items:
        img = item.img_tensor.to(device)
        caption = item.expressions

        pred = model(img, caption)
        user_items_vector.append(pred)

    candidate_items_vector = []
    for item in candidate_items:
        img = item.img_tensor.to(device)
        caption = item.expressions

        pred = model(img, caption)
        candidate_items_vector.append(pred)
    scores = []
    for i in user_items_vector:
        s = 0
        for index, j in enumerate(candidate_items_vector):
            s += torch.norm(i - j).item()
        scores.append(s if closest else 1 / s)
    return scores


def change_item_recommandation(cw: CapsuleWardrobe):
    # 全てのアイテムが一つ多い
    # 一番最後に推薦するアイテムが入っている
    initial_items = {
        "tops": cw.get_tops()[:-1],
        "bottoms": cw.get_bottoms()[:-1],
        "shoes": cw.get_shoes()[:-1],
    }
    remove_item_indexes = {"tops": None, "bottoms": None, "shoes": None}

    for k, item_list in zip(
        ["tops", "bottoms", "shoes"], [cw.get_tops(), cw.get_bottoms(), cw.get_shoes()]
    ):
        worst_item_score = (0, None)
        for i, _ in enumerate(item_list):
            copy_items = copy.deepcopy(initial_items)
            remove_item_list = copy.deepcopy(item_list)
            remove_item_list.pop(i)
            copy_items[k] = remove_item_list
            cw = CapsuleWardrobe(initial_items=copy_items)
            cw_score = cw.calc_self_cw_compatibility() + cw.calc_self_cw_versatility()
            if worst_item_score[0] < cw_score:
                worst_item_score = (cw_score, i)
                # print(worst_item_score, k, i)
        remove_item_indexes[k] = worst_item_score[1]
    return remove_item_indexes
