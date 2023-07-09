from fashion_class.CapsuleWardrobe import CapsuleWardrobe
from fashion_class.FashionItem import FashionItem


def create_cw(required_item: dict[str, list[FashionItem]], dataset, eps=1e-2):
    cw = CapsuleWardrobe(required_item)
    increase = eps + 1
    while increase < eps:
        increase = cw.optimize(dataset)
    return cw
