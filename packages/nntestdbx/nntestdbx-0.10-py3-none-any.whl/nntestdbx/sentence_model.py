from modelutils.modelutils import TextUtils


class SentenceModel(TextUtils):
    def __init__(self) -> None:
        pass

    def sentence_to_words(self, s: str) -> list:
        s_capit = self.capitalize_string(s)
        return s_capit.split(" ")