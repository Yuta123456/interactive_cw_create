
import random
from fashion_class.Coordinate import Coordinate
from fashion_class.FashionItem import FashionItem
import heapq

from fashion_class.ImageStruct import ImageStruct

class CapsuleWardrobe():
    def __init__(self, initial_items: dict[str, list[FashionItem]] = None, required_item: dict[str, list[FashionItem]] = None, max_length=4):
        if initial_items:
            self.tops = initial_items["tops"]
            self.bottoms = initial_items["bottoms"]
            self.shoes = initial_items["shoes"]

        if required_item:
            self.required_tops = required_item["tops"]
            self.required_bottoms = required_item["bottoms"]
            self.required_shoes = required_item["shoes"]

        self.coordinates = []
        self.score = 0
        self.c_weight = 1
        self.v_weight = 1
        self.item_cache_size = 10
        self.max_length = max_length
        
    def calc_self_cw_compatibility(self):
        self.create_coordinates()
        score = 0
        for c in self.coordinates:
            score += c.get_compatibility()
        self.score = score
        return self.score

    def calc_self_cw_versatility(self) -> int:
        score = 0
        for items in [self.tops, self.bottoms, self.shoes]:
            covered_cateogory = {[i.get_cover_category() for i in items]}
            score += len(covered_cateogory)
        return score

    def create_coordinates(self):
        coordinates: list[Coordinate] = []
        for t in self.tops + self.required_tops:
            for b in self.bottoms + self.required_bottoms:
                for s in self.shoes + self.required_shoes:
                    coordinate = Coordinate(t, b, s)
                    coordinates.append(coordinate)
        self.coordinates = coordinates
        return self.coordinates

    def optimize(self, dataset: ImageStruct):
        pre_score = self.score

        self.optimize_tops(dataset.tops)
        self.optimize_bottoms(dataset.bottoms)
        self.optimize_shoes(dataset.shoes)
        score = self.calc_self_cw_compatibility()
        self.score = score
        # TODO
        return score - pre_score
    
    def optimize_tops(self, dataset :list[FashionItem]):
        self.tops = []
        heap = []
        items = {}
        items["bottoms"] = self.bottoms + self.required_bottoms
        items["shoes"] = self.shoes + self.required_shoes
        for _ in range(self.max_length - len(self.required_tops)):
            for t in dataset:
                items["tops"] = [t]
                compatibility = self.calc_compatibility_increase(items)
                versatility = self.calc_versatility_increase(self.tops + self.required_tops, t)
                score = self.c_weight * compatibility + self.v_weight * versatility
                heapq.heappush(heap, (score, t))
                if len(heap) > self.item_cache_size:
                    heapq.heappop(heap)
            # ここはheapの最大値を持ってくる必要がある
            self.tops.append(max(heap, key=lambda x: x[0])[1])
        
    
        
    def optimize_bottoms(self, dataset):
        self.bottoms = []
        heap = []
        items = {}
        items["tops"] = self.tops + self.required_tops
        items["shoes"] = self.shoes + self.required_shoes
        for _ in range(self.max_length - len(self.required_bottoms)):
            for b in dataset:
                items["bottoms"] = [b]
                compatibility = self.calc_compatibility_increase(items)
                versatility = self.calc_versatility_increase(self.bottoms + self.required_bottoms, b)
                score = self.c_weight * compatibility + self.v_weight * versatility
                heapq.heappush(heap, (score, b))
                if len(heap) > self.item_cache_size:
                    heapq.heappop(heap)
            self.bottoms.append(max(heap, key=lambda x: x[0])[1])

    def optimize_shoes(self, dataset):
        self.shoes = []
        heap = []
        items = {}
        items["tops"] = self.tops + self.required_tops
        items["bottoms"] = self.bottoms + self.required_bottoms
        for _ in range(self.max_length - len(self.required_shoes)):
            for s in dataset:
                items["shoes"] = [s]
                compatibility = self.calc_compatibility_increase(items)
                versatility = self.calc_versatility_increase(self.shoes + self.required_shoes, s)
                score = self.c_weight * compatibility + self.v_weight * versatility
                
                heapq.heappush(heap, (score, s))
                if len(heap) > self.item_cache_size:
                    heapq.heappop(heap)
            self.shoes.append(max(heap, key=lambda x: x[0])[1])

    def calc_compatibility_increase(self, items):
        score = 0
        for t in items["tops"]:
            for b in items["bottoms"]:
                for s in items["shoes"]:
                    score += Coordinate(t, b, s).get_compatibility()
        return score
    
    def calc_versatility_increase(self, items: list[FashionItem], new_item: FashionItem):
        covered_cateogory = {[i.get_cover_category() for i in items]}
        pre_score = len(covered_cateogory)
        covered_cateogory.add(new_item.get_category)

        return len(covered_cateogory) - pre_score

    def show_images(self):
        # TODO: implements
        return

    def get_tops(self):
        return self.required_tops + self.tops

    def get_bottoms(self):
        return self.required_bottoms + self.bottoms

    def get_shoes(self):
        return self.required_shoes + self.shoes