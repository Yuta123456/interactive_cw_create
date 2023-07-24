import sys
#sys.path.append("fashion-clip/")
from fashion_clip.fashion_clip import FashionCLIP
import pandas as pd
import numpy as np
from collections import Counter
from PIL import Image
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from sklearn.linear_model import LogisticRegression

category_label = ['Vest top' 'Hair/alice band' 'Leggings/Tights' 'T-shirt' 'Sneakers'
 'Sunglasses' 'Cardigan' 'Gloves' 'Underwear Tights' 'Hoodie' 'Other shoe'
 'Shorts' 'Jumpsuit/Playsuit' 'Dress' 'Trousers' 'Belt' 'Socks'
 'Underwear bottom' 'Bodysuit' 'Hat/beanie' 'Scarf' 'Jacket'
 'Other accessories' 'Bra' 'Swimwear bottom' 'Blazer' 'Top' 'Polo shirt'
 'Sweater' 'Necklace' 'Pyjama set' 'Blouse' 'Bag' 'Shirt' 'Coat' 'Boots'
 'Skirt' 'Garment Set' 'Bikini top' 'Sandals' 'Dungarees' 'Earring'
 'Cap/peaked' 'Ballerinas' 'Swimsuit' 'Hat/brim']

color_label = []


# imagesは画像へのシンプルなリストでOK
fclip = FashionCLIP('fashion-clip')
label_embeddings = fclip.encode_text(labels_prompt, batch_size=32)
label_embeddings = label_embeddings/np.linalg.norm(label_embeddings, ord=2, axis=-1, keepdims=True)