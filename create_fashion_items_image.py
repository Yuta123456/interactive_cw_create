from PIL import Image, ImageDraw, ImageFont
from fashion_class.CapsuleWardrobeClass import CapsuleWardrobe

from fashion_class.FashionItem import FashionItem

def create_fashion_items_image(fashion_items: list[FashionItem]):
    images = []

    # 画像を読み込んでリストに追加する
    for item in fashion_items:
        image = Image.open(item.img_path)
        images.append(image)

    # 画像の幅と高さを取得
    width, height = images[0].size

    # 隙間として使用するピクセル数を定義
    gap = 5

    # 結合された画像の幅と高さを計算
    combined_width = width * 5 + gap * 4
    # item_idの分のgapを追加
    combined_height = (gap + 30 + height) * 2 

    input_image = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))
    # input_image.paste(images[0], (0, 0))
    # 元画像と「入力」という文字列を結合した画像を作成
    for i, image in enumerate(images):
        x = (i % 5) * (width + gap)
        y = (i // 5) * (height + gap) + 30 * ((i // 5)+1)

        input_image.paste(image, (x, y))

        # input_text = fashion_items[i].item_id
        text_color = (0, 0, 0)  # テキストの色を黒に設定
        text_font = ImageFont.truetype("arial.ttf", 16, encoding='utf-8')  # テキストのフォントとサイズを設定
        draw = ImageDraw.Draw(input_image)
        # text_width, text_height = draw.textsize(input_text, font=text_font)
        text_x = x  + 20 # 右端から5ピクセルの余白を開ける
        text_y = y - 20  # 元画像の上部中央に配置する
        draw.text((text_x, text_y), str(i+1), font=text_font, fill=text_color)
    return input_image

def create_cw_image(cw: CapsuleWardrobe):
    images = []

    item_size = cw.max_length
    all_items = cw.get_tops() + cw.get_bottoms() + cw.get_shoes()
    # 画像を読み込んでリストに追加する
    for item in all_items:
        image = Image.open(item.img_path)
        images.append(image)

    # 画像の幅と高さを取得
    width, height = images[0].size

    # 隙間として使用するピクセル数を定義
    gap = 5

    # 結合された画像の幅と高さを計算
    combined_width = ( width + gap ) * item_size
    # categoryの分のgapを追加
    combined_height = (gap + 30 + height) * 3

    input_image = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))

    for i, image in enumerate(images):
        x = (i % item_size) * (width + gap)
        y = (i // item_size) * (height + gap) + 30 * ((i // item_size)+1)

        input_image.paste(image, (x, y))

    draw = ImageDraw.Draw(input_image)
    for i, input_text in enumerate(["tops", "bottoms", "shoes"]):
        text_color = (0, 0, 0)  # テキストの色を黒に設定
        text_font = ImageFont.truetype("arial.ttf", 16, encoding='utf-8')  # テキストのフォントとサイズを設定
        # text_width, text_height = draw.textsize(input_text, font=text_font)
        text_x = 20 # 右端から5ピクセルの余白を開ける
        text_y = (gap + 30 + height) * i + 10 # 元画像の上部中央に配置する
        # print(text_x, text_y, input_text)
        draw.text((text_x, text_y), input_text, font=text_font, fill=text_color)
    return input_image

# item = {}
# item["tops"] = [FashionItem(i) for i in [
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/11258659_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/29580415_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/33636521_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/33636521_m.jpg",
# ]]
# item["bottoms"] = [FashionItem(i) for i in [
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/11258659_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/29580415_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/33636521_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/33636521_m.jpg",
# ]]
# item["shoes"] = [FashionItem(i) for i in [
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/11258659_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/29580415_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/33636521_m.jpg",
#         "D:/M1/fashion/IQON/IQON3000/1000092/3933191/33636521_m.jpg",
# ]]
# cw = CapsuleWardrobe(item)
# create_cw_image(
#     cw
# ).save('fashion.png')