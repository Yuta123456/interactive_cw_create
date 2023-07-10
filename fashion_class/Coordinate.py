from fashion_class.FashionItem import FashionItem
import json
from PIL import Image, ImageDraw, ImageFont

with open('../data/tops_count.json', 'r', encoding='shift-jis') as f:
    tops_compatibility = json.load(f)

# with open('../data/bottoms_count.json', 'r', encoding='shift-jis') as f:
#     bottoms_compatibility = json.load(f)

# with open('../data/shoes_count.json', 'r', encoding='shift-jis') as f:
#     shoes_compatibility = json.load(f)


class Coordinate():
    def __init__(self, tops: FashionItem, bottoms: FashionItem, shoes: FashionItem):
        self.tops = tops
        self.bottoms = bottoms
        self.shoes = shoes
        # compatibility計算
        self.compatibility = self.calc_compatibilty()
    
    def get_compatibility(self):
        return self.compatibility
    
    def create_coordinate_image(self):
        # 画像を読み込んでリストに追加する
        images = []
        for item in [self.tops,  self.bottoms, self.shoes]:
            image = Image.open(item.img_path)
            images.append(image)

        # 画像の幅と高さを取得
        width, height = images[0].size

        # 隙間として使用するピクセル数を定義
        gap = 5

        # 結合された画像の幅と高さを計算
        combined_width = width + gap * 2

        # tops, bottoms, shoesの分
        combined_height = (gap + height) * 3 + 46

        input_image = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))

        # 元画像と「入力」という文字列を結合した画像を作成
        for i, image in enumerate(images):
            x = gap
            # 46は、15 * 2 + 16(fontsize)
            y = i * (height + gap) + 46

            input_image.paste(image, (x, y))

        text_color = (0, 0, 0)  # テキストの色を黒に設定
        text_font = ImageFont.truetype("arial.ttf", 16, encoding='utf-8')  # テキストのフォントとサイズを設定
        draw = ImageDraw.Draw(input_image)
        # text_width, text_height = draw.textsize(input_text, font=text_font)
        text_x = gap # 右端から5ピクセルの余白を開ける
        text_y = 15  # 元画像の上部中央に配置する
        draw.text((text_x, text_y), f'{self.get_compatibility():.3f}', font=text_font, fill=text_color)
        return input_image

    # def calc_compatibilty(self):
    #     # この辺のエラーハンドリング
    #     # P(t | b, s)を計算
    #     compatibility = 0
    #     try:
    #         all_event = sum(tops_compatibility[self.bottoms.category][self.shoes.category].values())
    #         target_probability = tops_compatibility[self.bottoms.category][self.shoes.category][self.tops.category]
    #         compatibility += 0 if not target_probability else target_probability / all_event
    #     except KeyError:
    #         pass
        
    #     # P(b | t, s)を計算
    #     try:
    #         all_event = sum(bottoms_compatibility[self.tops.category][self.shoes.category].values())
    #         target_probability = bottoms_compatibility[self.tops.category][self.shoes.category][self.bottoms.category]
    #         compatibility += 0 if not target_probability else target_probability / all_event
    #     except KeyError:
    #         pass

    #     # P(s | t, b)を計算
    #     try:
    #         all_event = sum(shoes_compatibility[self.tops.category][self.bottoms.category].values())
    #         target_probability = shoes_compatibility[self.tops.category][self.bottoms.category][self.shoes.category]
    #         compatibility += 0 if not target_probability else target_probability / all_event
    #     except KeyError:
    #         pass
    #     return compatibility
    def calc_compatibilty(self):
        compatibility = 0
        try:
            compatibility += tops_compatibility[self.bottoms.category][self.shoes.category][self.tops.category]
        except KeyError:
            pass
        return compatibility

    def __eq__(self, other):
        return True