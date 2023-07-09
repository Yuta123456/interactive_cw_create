import torch
import pandas as pd

class CapsuleWardrobe():
    def __init__(self, requied_item_id: dict[str, list[str]] = None):
        self.tops = []
        self.bottoms = []
        self.shoes = []
        if requied_item_id:
            self.tops = requied_item_id["tops"]
            self.bottoms = requied_item_id["bottoms"]
            self.shoes = requied_item_id["shoes"]

    def calc_compatibility(self):
        coordinates = []
        
        

    