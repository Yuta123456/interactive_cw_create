from ImageStruct import ImageStruct
from create_cw import create_cw
from embedding_word import get_embedding_word
from fashion_class.FashionItem import FashionItem
from get_caption_model import get_caption_model
from search_items_from_caption_embedding import search_items_from_caption_embedding


# modelを定義
caption_model, tokenizer = get_caption_model()

# データセットを初期化
annotation_file, tensor_file = \
      './anotation_new.csv', './resnet50_tensor.pt'
dataset = ImageStruct(annotation_file, tensor_file)

# ユーザに表示して、気に入ったアイテムをいくつか選んでもらう
category_list = ["tops", "bottoms", "shoes"]
favorite_item_ids = {}
for c in category_list:
    favorite_item_ids[c] = []
    # 好きな単語をいくつか入力してもらう
    favorite_word = input("{c} を選びます。単語をスペース区切りで入力してください: ")
    # captionのベクトル化を行い、それに合う画像を検索
    caption_embedding = get_embedding_word(favorite_word, caption_model, tokenizer)

    # imagesは、このような形式
    # (-score, t_img_path, t_id)
    images = search_items_from_caption_embedding(caption_embedding, dataset)

    favorite_item_set = set(input('気に入った {c} アイテムのidをスペース区切りで入力してください').split())
    for _score, img_path, item_id in images:
        if item_id in favorite_item_set:
            favorite_item_ids[c].append(FashionItem(img_path))

# CWを構築
print("与えられた情報ををもとにCWを構築しています。")

cw = create_cw(required_item=favorite_item_ids)

print("生成されたcwがこちらです")

# 画像を表示

print("出来上がったcwに対して、【itemid: ~~】のような形式で要望を入れてください")