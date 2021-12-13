import random
from typing import *
from enum import Enum
from utils import *
from copy import deepcopy
from aligner import *
from dto.fragment import *
from settings import *


class Sample:
    def __init__(self, ru: Fragment = None, en: Fragment = None):
        self.id = str(uuid.uuid4())
        self.ru = ru
        self.en = en
        self.details = {}

    def add_to_the_left(self, prefix):
        self.ru.add_to_the_left(prefix.ru)
        self.en.add_to_the_left(prefix.en)

    def add_to_the_right(self, suffix):
        self.ru.add_to_the_right(suffix.ru)
        self.en.add_to_the_right(suffix.en)

    def add_trash(self, trash_path: str, left_proba: float = 0, right_proba: float = 0):
        left_monet = random.random()
        right_monet = random.random()
        if left_monet <= left_proba:
            prefix = create_random_simple_sample(trash_path)
            self.add_to_the_left(prefix)
        if right_monet <= right_proba:
            suffix = create_random_simple_sample(trash_path)
            self.add_to_the_right(suffix)

    def transfer_root(self, target_language: Language):
        tokens = self.en.tokens if target_language is Language.RU else self.ru.tokens
        root_mask = self.en.root_mask if target_language is Language.RU else self.ru.root_mask
        root_tokens = [_t for i, _t in enumerate(tokens) if root_mask[i] == 1]
        if target_language is Language.RU:
            self.ru.root_mask = extract_corresponding_mask(root_tokens, self.ru.tokens)
        else:
            self.en.root_mask = extract_corresponding_mask(root_tokens, self.en.tokens)


def create_random_simple_sample(file_path: str) -> Sample:
    sample_dict = sample_from_csv(file_path)
    ru_fragment = Fragment(sample_dict["ru"], Language.RU)
    en_fragment = Fragment(sample_dict["en"], Language.EN)
    sample = Sample(ru=ru_fragment, en=en_fragment)
    return sample


def create_random_root_sample(file_path: str) -> Sample:
    sample = create_random_simple_sample(file_path)
    sample.ru.turn_into_root()
    sample.en.turn_into_root()
    return sample


def create_random_sample_by_root(root_sample: Sample, trash_path: str,
                                 left_proba: float = 0, right_proba: float = 0) -> Sample:
    sample = deepcopy(root_sample)
    sample.add_trash(trash_path, left_proba=left_proba, right_proba=right_proba)
    return sample


def translate_sample(sample, model, source_language: Language, target_language: Language) -> Sample:
    source_fragment = sample.ru if source_language is Language.RU else sample.en
    translated_fragment = translate_fragment(source_fragment, model, source_language, target_language)
    if source_language is Language.RU:
        sample = Sample(ru=source_fragment, en=translated_fragment)
    else:
        sample = Sample(en=source_fragment, ru=translated_fragment)
    sample.transfer_root(target_language)
    return sample


if __name__ == "__main__":
    sample = create_random_root_sample(ROOT_FILE)
    sample.add_trash(TM_TRASH_FILE, left_proba=0, right_proba=1)
    a = 7
