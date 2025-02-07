import time

from pinecone import Pinecone, ServerlessSpec, PineconeApiException
from embedder import Embedder
from dotenv import load_dotenv
import pandas as pd
import json
import re
import os


load_dotenv()



index_name = "cocktails-1"

pc = Pinecone(os.environ.get("PINECONE_API_KEY"))

try:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws',
                            region='us-east-1')
    )
except PineconeApiException:
    pass

def get_prompt_from_df_row(row: pd.Series):
    def str_from_list(ings: str, measures: str):
        ings = ings.replace("\'", "\"")
        measures = measures.replace("\'", "\"")
        ings_list = re.findall("(?<=\")[^,]+?(?=\")", ings)
        measures_list = re.findall("(?<=\")[^,]+?(?=\")|None", measures)
        prompt = ""
        for i, m in zip(ings_list, measures_list):
            if len(prompt) != 0:
                prompt += ", "
            prompt += f"{i} - {m if m != 'None' else 'Not constant'}"
        return prompt

    prompt = f"{row['alcoholic']} cocktail {row['name']}, is a {row['category']} served in {row['glassType']}, " \
             f"it's ingredients are {str_from_list(row['ingredients'], row['ingredientMeasures'])}, " \
             f"serving instructions are: {row['instructions']}"
    return prompt


cocktails_df = pd.read_csv("final_cocktails.csv", index_col=0).set_index('id')
cocktail_prompt_series = cocktails_df.apply(get_prompt_from_df_row, axis=1).to_list()


while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)


model = Embedder(os.environ.get("EMBEDDING_MODEL_NAME"))
embeddings = model.get_embeddings(cocktail_prompt_series)

index = pc.Index(index_name)
vectors = []
for i, (d, e) in enumerate(zip(cocktail_prompt_series, embeddings)):
    vectors.append({
        'id': f"vec{i}",
        'values': e,
        'metadata': {"text": d}
    })

index.upsert(vectors, namespace='ckts1')