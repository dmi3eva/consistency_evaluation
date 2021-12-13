# from transformers import BertTokenizer
# tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

from simalign import SentenceAligner
aligner = SentenceAligner(token_type='bpe')