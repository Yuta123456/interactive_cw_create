import random
from fashion_class.FashionItem import FashionItem
import json

with open('./data/tops_count.json', 'r', encoding='shift-jis') as f:
    tops_compatibility = json.load(f, ensure_ascii=False)

with open('./data/bottoms_count.json', 'r', encoding='shift-jis') as f:
    bottoms_compatibility = json.load(f, ensure_ascii=False)

with open('./data/shoes_count.json', 'r', encoding='shift-jis') as f:
    shoes_compatibility = json.load(f, ensure_ascii=False)


class Coordinate():
    def __init__(self, tops: FashionItem, bottoms: FashionItem, shoes: FashionItem):
        self.tops = tops
        self.bottoms = bottoms
        self.shoes = shoes
        # compatibility計算
        self.compatibility = self.calc_compatibilty()
    
    def get_compatibility(self):
        return self.compatibility
    
    def show_coordinate(self):
        # TODO: implements
        return
    def calc_compatibilty(self):
        # P(t | b, s)を計算
        compatibility = 0
        all_event = sum(tops_compatibility[self.bottoms.category][self.shoes.category].values())
        target_probability = tops_compatibility[self.bottoms.category][self.shoes.category][self.tops.category]
        compatibility += 0 if not target_probability else target_probability / all_event
        
        # P(b | t, s)を計算
        all_event = sum(bottoms_compatibility[self.tops.category][self.shoes.category].values())
        target_probability = bottoms_compatibility[self.tops.category][self.shoes.category][self.bottoms.category]
        compatibility += 0 if not target_probability else target_probability / all_event

        # P(s | t, b)を計算
        all_event = sum(shoes_compatibility[self.tops.category][self.bottoms.category].values())
        target_probability = shoes_compatibility[self.tops.category][self.bottoms.category][self.shoes.category]
        compatibility += 0 if not target_probability else target_probability / all_event

        return compatibility