import random
import uuid

from typing import *
from enum import Enum
from utils import *
from copy import deepcopy
from aligner import *
from dto.fragment import *
from settings import *

import nltk.translate.bleu_score as bleu

from SberTMT.utils import Language

# class Language(Enum):
#     EN = 0
#     RU = 1


class Fragment:
    def __init__(self, text: str, language: Language, tokens: List[str] = None, root_pos: List[int] = None):
        self.text = text
        self.language = language
        self.tokens = tokens
        self.root_mask = root_pos
        if not self.tokens:
            self.tokens = tokenize(text)
        if not self.root_mask:
            self.root_mask = [0 for _ in self.tokens]

    def turn_into_root(self):
        self.root_mask = [1 for _ in self.tokens]

    def add_to_the_left(self, prefix):
        self.text = prefix.text + " " + self.text
        self.tokens = prefix.tokens + self.tokens
        self.root_mask = prefix.root_mask + self.root_mask

    def add_to_the_right(self, suffix):
        self.text = self.text + " " + suffix.text
        self.tokens = self.tokens + suffix.tokens
        self.root_mask = self.root_mask + suffix.root_mask

    @property
    def root_tokens(self) -> List[str]:
        root_tokens = [_t for i, _t in enumerate(self.tokens) if self.root_mask[i] == 1]
        return root_tokens

    @property
    def root_text(self) -> str:
        root_str = aligner.embed_loader.tokenizer.convert_tokens_to_string(self.root_tokens)
        return root_str

    @property
    def root_highlighted_as_source(self) -> str:
        formatted_tokens = [_t if not _m else f"<u>{_t}</u>" for _m, _t in zip(self.root_mask, self.tokens)]
        formatted_text = " ".join(formatted_tokens)
        return formatted_text

    @property
    def root_highlighted_as_translation(self) -> str:
        formatted_text = " "
        current_text = []
        last_state = None
        for _m, _t in zip(self.root_mask, self.tokens):
            if last_state is None or _m == last_state:
                current_text.append(_t)
            else:
                formatted_text = expand_formatted(formatted_text, current_text, last_state)
                current_text = [_t]
            last_state = _m
        formatted_text = expand_formatted(formatted_text, current_text, last_state)
        return formatted_text



def expand_formatted(formated_text: str, current_text: List[str], last_state: int) -> str:
    text = aligner.embed_loader.tokenizer.convert_tokens_to_string(current_text)
    if last_state == 1:
        text = f" <u>{text}</u>"
    formated_text += text
    return formated_text


def translate_fragment(fragment, model, source_language: Language, target_language: Language) -> Fragment:
    source = fragment.text
    translation = model.translate(source_language, target_language, source)
    return Fragment(translation, target_language)


def get_fragments_text_bleu(fragment_1: Fragment, fragment_2: Fragment) -> float:
    if fragment_1.language is not fragment_2.language:
        raise ValueError("Fragments are incomparable because of different languages.")
    score = bleu.sentence_bleu([fragment_1.tokens], fragment_2.tokens)
    return score


def get_fragments_root_bleu(fragment_1: Fragment, fragment_2: Fragment) -> float:
    if fragment_1.language is not fragment_2.language:
        raise ValueError("Fragments are incomparable because of languages.")
    root_1_tokens = [_t for i, _t in enumerate(fragment_1.tokens) if fragment_1.root_mask[i] == 1]
    root_2_tokens = [_t for i, _t in enumerate(fragment_2.tokens) if fragment_2.root_mask[i] == 1]
    score = bleu.sentence_bleu([root_1_tokens], root_2_tokens)
    return score



reference = [['This', 'is', 'a', 'test']]
candidate = ['this', 'is', 'a', 'test']
score = bleu.sentence_bleu(reference, candidate)
print(score)
