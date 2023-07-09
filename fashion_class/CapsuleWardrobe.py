from fashion_class.Coordinate import Coordinate
from fashion_class.FashionItem import FashionItem
import heapq

class CapsuleWardrobe():
    def __init__(self, required_item: dict[str, list[FashionItem]] = None, max_length=4):
        self.tops = []
        self.bottoms = []
        self.shoes = []
        self.coordinates = []
        self.score = 0
        self.max_length = max_length
        if required_item:
            self.required_tops = required_item["tops"]
            self.required_bottoms = required_item["bottoms"]
            self.required_shoes = required_item["shoes"]

    def calc_self_cw_compatibility(self):
        self.create_coordinates()
        score = 0
        for c in self.coordinates:
            score += c.get_compatibility()
        self.score = score
        return self.score


    def create_coordinates(self):
        coordinates: list[Coordinate] = []
        for t in self.tops + self.required_tops:
            for b in self.bottoms + self.required_bottoms:
                for s in self.shoes + self.required_shoes:
                    coordinate = Coordinate(t, b, s)
                    coordinates.append(coordinate)
        self.coordinates = coordinates
        return self.coordinates

    def optimize(self, dataset):
        pre_score = self.score

        self.optimize_tops(dataset["tops"])
        self.optimize_bottoms(dataset["bottoms"])
        self.optimize_shoes(dataset["shoes"])
        score = self.calc_self_cw_compatibility()
        return score - pre_score
    
    def optimize_tops(self, dataset):
        heap = []
        items = {}
        items["bottoms"] = self.bottoms + self.required_bottoms
        items["shoes"] = self.shoes + self.required_shoes
        for t in dataset:
            items["top"] = [t]
            score = self.calc_score_increase(items)
            heapq.heappush(heap, (-score, t))
            if len(heap) + len(self.required_tops) > self.max_length:
                heapq.heappop(heap)
        self.tops = [t[1] for t in heap]
        
    
        
    def optimize_bottoms(self, dataset):
        heap = []
        items = {}
        items["tops"] = self.tops + self.required_tops
        items["shoes"] = self.shoes + self.required_shoes
        for b in dataset:
            items["bottoms"] = [b]
            score = self.calc_score_increase(items)
            heapq.heappush(heap, (-score, b))
            if len(heap) + len(self.required_bottoms) > self.max_length:
                heapq.heappop(heap)
        self.tops = [b[1] for b in heap]

    def optimize_shoes(self, dataset):
        heap = []
        items = {}
        items["tops"] = self.tops + self.required_tops
        items["bottoms"] = self.bottoms + self.required_bottoms
        for s in dataset:
            items["shoes"] = [s]
            score = self.calc_score_increase(items)
            heapq.heappush(heap, (-score, s))
            if len(heap) + len(self.required_shoes) > self.max_length:
                heapq.heappop(heap)
        self.tops = [s[1] for s in heap]

    def calc_score_increase(self, items):
        score = 0
        for t in items["top"]:
            for b in items["bottoms"]:
                for s in items["bottoms"]:
                    score += Coordinate(t, b, s).get_compatibility()
        return score
    
    def show_images(self):
        # TODO: implements