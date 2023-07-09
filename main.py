from create_cw import create_cw
from embedding_word import get_embedding_word
from fashion_class.FashionItem import FashionItem
from fashion_class.ImageStruct import ImageStruct
from get_caption_model import get_caption_model
from search_items_from_caption_embedding import search_items_from_caption_embedding


# modelを定義
print('model初期化')
caption_model, tokenizer = get_caption_model()
print('model初期化完了')

print('データセット初期化中')
# データセットを初期化
annotation_file, tensor_file = \
      './data/anotation_new.csv', './data/resnet50_tensor.pt'
dataset = ImageStruct(annotation_file, tensor_file)
print('データセット初期化終了')
# ユーザに表示して、気に入ったアイテムをいくつか選んでもらう
category_list = ["tops", "bottoms", "shoes"]
favorite_items = {}
for c in category_list:
    favorite_items[c] = []
    # 好きな単語をいくつか入力してもらう
    favorite_word = input(f"{c} を選びます。単語をスペース区切りで入力してください: ")
    print(f'{favorite_word} に基づき、画像検索を行います。')
    # captionのベクトル化を行い、それに合う画像を検索
    caption_embedding = get_embedding_word(favorite_word, caption_model, tokenizer)

    # imagesは、このような形式
    # (-score, t_img_path, t_id)
    images = search_items_from_caption_embedding(caption_embedding, dataset)

    favorite_item_set = set(input(f'気に入った {c} アイテムのidをスペース区切りで入力してください').split())
    for _score, img_path, item_id in images:
        if item_id in favorite_item_set:
            favorite_items[c].append(FashionItem(img_path))

# CWを構築
print("与えられた情報をもとにCWを構築しています。")

cw = create_cw(favorite_items, dataset)

print("生成されたcwがこちらです")

# 画像を表示
cw.show_images()
item_id, comment = input("出来上がったcwに対して、itemid: ~~ のような形式で要望を入れてください > ").split(':')
