import torch
from category import get_image_info

# {
#     "imgUrl": "https://img.iqon.jp/items/27068307/27068307_m.jpg",
#     "price": "12,420",
#     "category x color": "ワンピース × 灰色（グレー）",
#     "itemId": 27068307,
#     "itemName": "[L]メリノウールニットロングワンピース",
#     "itemUrl": "https://item.iqon.jp/27068307/",
#     "breadcrumb": [
#         [
#             "IQONトップ",
#             "ブランドをさがす",
#             "アンタイトル［UNTITLED］",
#             "ワンピース",
#             "ニットワンピース",
#             "[L]メリノウールニットロングワンピース"
#         ],
#         [
#             "IQONトップ",
#             "カテゴリでさがす",
#             "ワンピース",
#             "ニットワンピース",
#             "[L]メリノウールニットロングワンピース"
#         ]
#     ],
#     "brands": [
#         "ブランド：アンタイトル［UNTITLED］"
#     ],
#     "categorys": [
#         "カテゴリ：アンタイトル［UNTITLED］× ワンピースアンタイトル［UNTITLED］× ニットワンピース"
#     ],
#     "options": [
#         "素材：ウールウール × ワンピースウール × ニットワンピース",
#         "着丈：ロング丈ロング丈 × ワンピースロング丈 × ニットワンピース"
#     ],
#     "colors": [
#         "色：灰色（グレー）× ワンピース灰色（グレー）× ニットワンピース"
#     ],
#     "expressions": [
#         "アイテム説明程よい厚みのある、ロング丈のニットワンピース。ゆるめのオフタートルや、裾のスリットが、今年らしい印象です。脇に縫い目のない、ホールガーメント(R)仕様で、着心地の良さも嬉しい。膨らみと軽さがあり、暖かい着心地を感じられるニット素材を使用しています。※着丈が11cm短くなります。モデル情報：身長172cm B80 W60 H85 着用サイズ：02サイズ違いの商品もご用意しております。R:153-59551店舗へのお問い合わせ商品番号：153-59001主に冬に着用いただける商品です。【送料】全国一律400円（税込）。10,000円（税込）以上購入で送料無料。\r\n【配送期間】購入完了より約3日内発送\r\n【ポイント】購入金額(税抜)の100円に付き1ポイントが加算(対象外商品あり)。1ポイント=1円として購入時に利用可能。\r\n※記載事項に関しまして、購入サイトにて変更が生じる場合がございます。さらにくわしい情報をみる"
#     ]
# },

cluster_tensors = torch.load('D:/M1/fashion/optimization/data/center_tensors.pt')

class FashionItem():
    def __init__(self, img_path: str, img_tensor):
        self.img_path = img_path
        self.img_tensor = img_tensor
        self.item_info = get_image_info(img_path)
        self.item_id = self.item_info["itemId"]
        self.category = self.item_info["category x color"]
        self.cover_category = None
    
    def get_category(self):
        garment = self.category.split(' × ')[0]
        if garment in ["ジャケット", "トップス", "コート", "ニット", "タンクトップ", "ブラウス", "Tシャツ", "カーディガン", "ダウンジャケット", "パーカー"]:
            return "tops"
            # , "ショートパンツ"入れ忘れた
        if garment in ['スカート', 'ロングスカート', "ロングパンツ"]:
            return "bottoms"
        
        if garment in ["ブーツ", "パンプス", "スニーカー", "靴", "サンダル"]:
            return "shoes"
        
        return "others"
    
    def get_cover_category(self) -> int:
        # cluster_tensors に対して距離を図り、一番近いもののラベルを返す
        if self.cover_category:
            return self.cover_category

        X = self.img_tensor.expand(cluster_tensors.size())

        # ユークリッド距離を計算します
        distances = torch.sqrt(torch.sum((X - cluster_tensors) ** 2, dim=1))

        # 最小距離のインデックスを見つけます
        label = torch.argmin(distances).item()
        self.cover_category = label
        return label

