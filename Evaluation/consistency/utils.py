import random

import pandas as pd
from settings import *
from nlp_storage import aligner
from simalign import SentenceAligner


def tokenize(text):
    tokens = aligner.embed_loader.tokenizer.tokenize(text)
    return tokens


def sample_from_csv(file_path):
    data = pd.read_csv(file_path, encoding="utf-8")
    rows_amount = data.shape[0]
    if "used" not in data.columns:
        data["used"] = [False for _ in range(rows_amount)]
    not_used = data[data["used"] == False]
    not_used_indices = list(not_used.index)
    if len(not_used_indices) == 0:
        raise ValueError(f"In {file_path} all samples are used.")
    sampled_ind = random.choice(not_used_indices)
    data.loc[sampled_ind, 'used'] = True
    sample = data.loc[sampled_ind].to_dict()
    del sample['Unnamed: 0']
    del sample['used']
    data.to_csv(file_path, encoding="utf-8")
    return sample


if __name__ == "__main__":
    sample = tokenize("Hello! I am Katya. And now i am still alive")
    a = 7
