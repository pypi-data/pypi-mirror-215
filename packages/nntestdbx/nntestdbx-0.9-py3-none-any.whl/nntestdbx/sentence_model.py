from modelutils.modelutils import TextUtils


class SentenceModel(TextUtils):
    def __init__(self) -> None:
        pass

    @staticmethod
    def sentence_to_words(s: str) -> list:
        s_capit = self.capitalize_string(s)
        return s_capit.split(" ")