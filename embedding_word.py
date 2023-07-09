import torch
def get_embedding_word(word, caption_model, tokenizer):
    if torch.cuda.is_available():
        device = torch.device("cuda")  # GPUデバイスを取得
    else:
        device = torch.device("cpu")  # CPUデバイスを取得
    ids = tokenizer.encode(word, return_tensors='pt', padding='max_length', truncation=True, max_length=256, add_special_tokens=True)
    ids = ids.to(device)
    caption_tensor = caption_model(ids).to('cpu')
    return caption_tensor
