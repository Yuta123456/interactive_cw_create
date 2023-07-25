import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn as nn

class CaptionEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModel.from_pretrained("cl-tohoku/bert-base-japanese-v2")
    
    def forward(self, x):
        x = self.bert(x)
        x = x.last_hidden_state
        x = x[:,0,:] 
        return x

def get_caption_model():
    if torch.cuda.is_available():
        device = torch.device("cuda")  # GPUデバイスを取得
    else:
        device = torch.device("cpu")  # CPUデバイスを取得

    # D:\M1\fashion\optimization\model
    model_name =  'D:/M1/fashion/optimization/model/model_caption_2023-07-08.pth'
    caption_model = CaptionEncoder().to(device)
    caption_model.load_state_dict(torch.load(model_name))
    caption_model.eval()

    tokenizer = AutoTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-v2")
    return caption_model, tokenizer