from dto.root_brood import *


class RootTranslation:
    def __init__(self, root_brood, model, source: Language, target: Language):
        self.root_brood = root_brood
        self.model = model
        self.source = source
        self.target = target
        self.root_translation = None
        self.contains_translation = None
        self.text_bleus = None
        self.root_bleus = None
        self.target_root = None
        self.target_fragments = None

    def translate_root(self):
        if not self.root_translation:
            self.root_translation = translate_sample(self.root_brood, self.model, self.source, self.target)

    def translate_contains(self):
        if not self.contains_translation:
            self.contains_translation = [translate_sample(_s, self.model, self.source, self.target)
                                         for _s in self.root_brood.contains]
        if self.target is Language.EN:
            self.target_root = self.root_brood.root.en
            self.target_fragments = [_s.en for _s in self.contains_translation]
        else:
            self.target_root = self.root_brood.ru
            self.target_fragments = [_s.ru for _s in self.contains_translation]

    def calculate_bleus(self):
        self.translate_contains()
        if not self.text_bleus:
            self.text_bleus = [get_fragments_text_bleu(self.target_root, _s) for _s in self.target_fragments]
        if not self.root_bleus:
            self.root_bleus = [get_fragments_root_bleu(self.target_root, _s) for _s in self.target_fragments]

    @property
    def avg_text_bleu(self) -> float:
        if not self.text_bleus:
            self.calculate_bleus()
        return sum(self.text_bleus) / len(self.text_bleus)

    @property
    def avg_root_bleu(self) -> float:
        if not self.root_bleus:
            self.calculate_bleus()
        return sum(self.root_bleus) / len(self.root_bleus)

    @property
    def translated_roots(self) -> List[str]:
        self.translate_contains()
        roots = [_s.root_text  for _s in self.target_fragments]
        return roots

    @property
    def formated_translation(self) -> List[str]:
        self.translate_contains()
        formated = [_s.formatted_text for _s in self.target_fragments]
        return formated


    @property
    def pretty_formated_translation(self) -> List[str]:
        self.translate_contains()
        formated = [_s.root_highlighted_as_translation for _s in self.target_fragments]
        return formated
