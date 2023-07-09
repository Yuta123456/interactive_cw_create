import pandas as pd


def get_image_category(img_path: str):
    img_path = img_path.replace('\\', '/')
    coordinate_info = get_coordinate_info(img_path)
    fashion_item_id = img_path.split('/')[-1]
    # itemsの中のidに一致するものを探す
    for item in coordinate_info['items']:
        if item['itemId'] == int(fashion_item_id.split('_')[0]):
            return item['category x color']

    
def get_coordinate_info(img_path: str):
    coordinate_id = img_path.split('/')[-2]
    coordinate_json_path = '/'.join(img_path.split('/')[:-1]) + '/' + coordinate_id + '_new.json'
    try:
        d = open(coordinate_json_path, 'r', encoding='shift-jis')
        json_data = pd.read_json(d, encoding='shift-jis')
    except Exception as e:
        print(e)
        return None
    return json_data

def get_item_id(img_path: str):
    # D:/M1/fashion/IQON/IQON3000\\1283890\\3606832/10755545_m.jpg
    img_path = img_path.replace('\\', '/')
    return img_path.split('/')[-1]