from fashion_class.FashionItem import FashionItem


class Coordinate():
    def __init__(self, tops: FashionItem, bottoms: FashionItem, shoes: FashionItem):
        self.tops = tops
        self.bottoms = bottoms
        self.shoes = shoes
        # compatibility計算
        self.compatibility = 0
    
    def get_compatibility(self):
        return self.compatibility
    
    def show_coordinate(self):
        # TODO: implements
        return