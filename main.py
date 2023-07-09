from ImageStruct import ImageStruct
from embedding_word import get_embedding_word
from get_caption_model import get_caption_model
from search_items_from_caption_embedding import search_items_from_caption_embedding


# 好きな単語をいくつか入力してもらう
favorite_word = input("単語をスペース区切りで入力してください: ")

# modelを定義
caption_model, tokenizer = get_caption_model()

# データセットを初期化
annotation_file, tensor_file = \
      './anotation_new.csv', './resnet50_tensor.pt'
dataset = ImageStruct(annotation_file, tensor_file)

# captionのベクトル化を行い、それに合う画像を検索
caption_embedding = get_embedding_word(favorite_word, caption_model, tokenizer)

images = search_items_from_caption_embedding(caption_embedding, dataset)

# ユーザに表示して、気に入ったアイテムをいくつか選んでもらう

favorite_item_ids = input('気に入ったアイテムのidをスペース区切りで入力してください').split()

# CWを構築
print("与えられた情報ををもとにCWを構築しています。")

cw = create_cw(required_item=favorite_item_ids)

print("生成されたcwがこちらです")

# 画像を表示

print("出来上がったcwに対して、【itemid: ~~】のような形式で要望を入れてください")