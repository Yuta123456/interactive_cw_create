from fashion_class.CapsuleWardrobe import CapsuleWardrobe
from fashion_class.FashionItem import FashionItem


def create_cw(required_item: dict[str, list[FashionItem]], dataset, eps=1e-2):
    cw = CapsuleWardrobe(required_item)
    increase = eps - 1
    roop = 0
    while increase < eps:
        print(f"{roop}回目 増加分: {increase}")
        increase = cw.optimize(dataset)
    return cw
