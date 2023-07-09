import random
from fashion_class.FashionItem import FashionItem


class Coordinate():
    def __init__(self, tops: FashionItem, bottoms: FashionItem, shoes: FashionItem):
        self.tops = tops
        self.bottoms = bottoms
        self.shoes = shoes
        # compatibility計算
        self.compatibility = random.random()
    
    def get_compatibility(self):
        return self.compatibility
    
    def show_coordinate(self):
        # TODO: implements
        return