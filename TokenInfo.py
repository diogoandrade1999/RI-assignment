
class TokenInfo:
    """
    Class used by tokenize the data with a simple tokenizer.

    ...

    Attributes
    ----------
    doc : str
        The document id.
    weight : int
        The weight of that token.
    """
    def __init__(self, doc, doc_freq, doc_len=0, positions=None):
        """
        Parameters
        ----------
        doc: str
            The document id.
        doc_freq : int
            The number of times we find that token on document.
        doc_len : int
            The number of tokens in the document.
        """
        self._doc = doc
        self._weight = doc_freq
        self._doc_len = doc_len
        self._positions = positions if positions else []

    @property
    def doc(self):
        return self._doc

    @property
    def weight(self):
        return self._weight

    @property
    def doc_len(self):
        return self._doc_len

    @property
    def positions(self):
        return self._positions

    @weight.setter
    def weight(self, new_weight):
        self._weight = new_weight

    def add_position(self, index):
        self._positions.append(index)
        self._weight += 1

    def __eq__(self, token):
        if token is None: return False

        if not isinstance(token, TokenInfo): return False

        return self._doc == token.doc

    def __hash__(self):
        return hash(self._doc)

    def __repr__(self):
        if self._doc_len > 0:
            if len(self._positions) > 0:
                return f"{self._doc},{self._doc_len}:{self._weight:.2f}{self._positions}"

            return f"{self._doc},{self._doc_len}:{self._weight:.2f}"

        if len(self._positions) > 0:
            return f"{self._doc}:{self._weight:.2f}{self._positions}"

        return f"{self._doc}:{self._weight:.2f}"

    def __str__(self):
        if self._doc_len >0:
            if len(self._positions) > 0:
                return f"{self._doc},{self._doc_len}:{self._weight:.2f}{self._positions}"

            return f"{self._doc},{self._doc_len}:{self._weight:.2f}"

        if len(self._positions) > 0:
            return f"{self._doc}:{self._weight:.2f}{self._positions}"

        return f"{self._doc}:{self._weight:.2f}"
