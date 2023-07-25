from PIL import Image, ImageDraw, ImageFont
import torch
from category import get_image_info


cluster_tensors = torch.load('D:/M1/fashion/optimization/data/center_tensors.pt')
# 
NEAREST_CATEGORY = 30
class FashionItem():
    def __init__(self, img_path: str, img_tensor):
        self.img_path = img_path
        self.img_tensor = img_tensor
        self.item_info = get_image_info(img_path)
        self.item_id = self.item_info["itemId"]
        self.category = self.item_info["category x color"]
        self.cover_category = None
    
    def get_category(self, garment = None):
        if garment == None:
            garment = self.category.split(' × ')[0]
        if garment in ["ジャケット", "トップス", "コート", "ニット", "タンクトップ", "ブラウス", "Tシャツ", "カーディガン", "ダウンジャケット", "パーカー"]:
            return "tops"
            # , "ショートパンツ"入れ忘れた
        if garment in ['スカート', 'ロングスカート', "ロングパンツ"]:
            return "bottoms"
        
        if garment in ["ブーツ", "パンプス", "スニーカー", "靴", "サンダル"]:
            return "shoes"
        
        return "others"
    
    def get_cover_category(self) -> list[int]:
        # cluster_tensors に対して距離を図り、一番近いもののラベルを返す
        if self.cover_category:
            return self.cover_category

        X = self.img_tensor.expand(cluster_tensors.size())

        # ユークリッド距離を計算します
        distances = torch.sqrt(torch.sum((X - cluster_tensors) ** 2, dim=1))
        # 上位k個の最小値のインデックスを取得
        sorted_indices = torch.argsort(distances)

        k_min_indices = sorted_indices[:NEAREST_CATEGORY]
        # print(k_min_indices)
        label: list[int] = k_min_indices.tolist()
        self.cover_category = label
        return label

    def create_image(self):
        # 画像を読み込んでリストに追加する
        image = Image.open(self.img_path)

        input_image = Image.new('RGB', (image.width, image.height + 30), (255, 255, 255))

        input_image.paste(image, (0, 30))

        text_color = (0, 0, 0)  # テキストの色を黒に設定
        text_font = ImageFont.truetype("arial.ttf", 16, encoding='utf-8')  # テキストのフォントとサイズを設定
        draw = ImageDraw.Draw(input_image)
        draw.text((30, 15), 'item', font=text_font, fill=text_color)
        return input_image

    def __eq__(self, other):
        return True
    def __lt__(self, other):
        return True
    def __gt__(self, other):
        return True
    def __le__(self, other):
        return True
    def __ge__(self, other):
        return True
