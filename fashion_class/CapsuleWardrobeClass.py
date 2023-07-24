
import random
from fashion_class.Coordinate import Coordinate
from fashion_class.FashionItem import FashionItem
import heapq
from itertools import chain
from fashion_class.ImageStruct import ImageStruct

# center_tensorは300クラスに分類されている
REGULER_VERSATILITY_SCORE = 4
LAYER = 3
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
            covered_cateogory = set(list(chain.from_iterable([i.get_cover_category() for i in items])))
            score += len(covered_cateogory)
        return score / (self.max_length * REGULER_VERSATILITY_SCORE)

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
        c, v = self.calc_self_cw_compatibility() / pow(self.max_length, LAYER),  self.calc_self_cw_versatility() / LAYER
        print(c, v)
        score = c + v
        self.score = score
        # TODO
        return score - pre_score
    
    def optimize_tops(self, dataset :list[FashionItem]):
        self.tops = []
        heap = []
        items = {}
        items["bottoms"] = self.get_bottoms()
        items["shoes"] = self.get_shoes()
        for _ in range(self.max_length - len(self.required_tops)):
            heap = []
            for t in dataset:
                if t.item_id in [i.item_id for i in self.get_tops()]:
                    continue
                items["tops"] = [t]
                compatibility = self.calc_compatibility_increase(items)
                versatility = self.calc_versatility_increase(self.get_tops(), t)
                score = self.c_weight * compatibility + self.v_weight * versatility
                heapq.heappush(heap, (score, t))
                if len(heap) > self.item_cache_size:
                    heapq.heappop(heap)
            # ここはheapの最大値を持ってくる必要がある
            self.tops.append(max(heap, key=lambda x: x[0])[1])
        assert len(self.get_tops()) == self.max_length
    
        
    def optimize_bottoms(self, dataset):
        self.bottoms = []
        heap = []
        items = {}
        items["tops"] = self.get_tops()
        items["shoes"] = self.get_shoes()
        for _ in range(self.max_length - len(self.required_bottoms)):
            heap = []
            for b in dataset:
                if b.item_id in [i.item_id for i in self.get_bottoms()]:
                    continue
                # if b.item_id == 9995388:
                #     print("hoge", [i.item_id for i in self.get_bottoms()])
                items["bottoms"] = [b]
                compatibility = self.calc_compatibility_increase(items)
                versatility = self.calc_versatility_increase(self.get_bottoms(), b)
                score = self.c_weight * compatibility + self.v_weight * versatility
                heapq.heappush(heap, (score, b))
                if len(heap) > self.item_cache_size:
                    heapq.heappop(heap)
            self.bottoms.append(max(heap, key=lambda x: x[0])[1])
        assert len(self.get_bottoms()) == self.max_length

    def optimize_shoes(self, dataset: list[FashionItem]):
        self.shoes = []
        heap = []
        items = {}
        items["tops"] = self.get_tops()
        items["bottoms"] = self.get_bottoms()
        for _ in range(self.max_length - len(self.required_shoes)):
            heap = []
            for s in dataset:
                if s.item_id in [i.item_id for i in self.get_shoes()]:
                    continue
                items["shoes"] = [s]
                compatibility = self.calc_compatibility_increase(items)
                versatility = self.calc_versatility_increase(self.get_shoes(), s)
                score = self.c_weight * compatibility + self.v_weight * versatility
                
                heapq.heappush(heap, (score, s))
                if len(heap) > self.item_cache_size:
                    heapq.heappop(heap)
            self.shoes.append(max(heap, key=lambda x: x[0])[1])

        assert len(self.get_shoes()) == self.max_length

    def calc_compatibility_increase(self, items):
        score = 0
        for t in items["tops"]:
            for b in items["bottoms"]:
                for s in items["shoes"]:
                    score += Coordinate(t, b, s).get_compatibility()
        return score
    
    def calc_versatility_increase(self, items: list[FashionItem], new_item: FashionItem):
        covered_cateogory = set(list(chain.from_iterable([i.get_cover_category() for i in items])))
        pre_score = len(covered_cateogory)
        covered_cateogory.add(new_item.get_category())

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