from transformers import AutoTokenizer, AutoModel
import torch

class Embedder:
    def __init__(self, model_path: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)

    def get_embeddings(self, data: list):
        tokenized_queries = self.tokenizer(data, padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            model_output = self.model(**tokenized_queries)
            embeddings = model_output[0][:, 0]

        embeddings = torch.nn.functional.normalize(embeddings, dim=1)
        return embeddings

