from simalign import SentenceAligner
from utils import tokenize

from nlp_storage import aligner


def extract_corresponding_mask(src_tokens, tgt_tokens, method='mwmf'):
    alignments = aligner.get_word_aligns(src_tokens, tgt_tokens)
    corr_pairs = alignments[method]
    corr_tokens = [_p[1] for _p in corr_pairs]
    corr_mask = [1 if i in corr_tokens else 0 for i, _ in enumerate(tgt_tokens)]
    return corr_mask
