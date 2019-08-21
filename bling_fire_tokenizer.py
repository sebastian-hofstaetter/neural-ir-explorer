from allennlp.data.tokenizers.token import Token
from blingfire import *
from typing import List


class BlingFireTokenizer():
    """
    basic tokenizer using bling fire library
    """

    def tokenize(self, sentence: str) -> List[str]:
        return text_to_words(sentence).split()
