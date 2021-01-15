
class TokenInfo:
    """
    Class used by tokenize the data with a simple tokenizer.

    ...

    Attributes
    ----------
    doc : str
        The document id.
    weight : float
        The weight of that token.
    doc_len : int
        The number of tokens in the document.
    positions : list
        The token positions inside the file.
    """
    def __init__(self, doc:str, weight:float, doc_len:int=0, positions:list=None):
        """
        Parameters
        ----------
        doc : str
            The document id.
        weight : float
            The weight of that token.
        doc_len : int
            The number of tokens in the document.
        positions : list
            The token positions inside the file.
        """
        self._doc = doc
        self._weight = weight
        self._doc_len = doc_len
        self._positions = positions if positions else []

    @property
    def doc(self) -> str:
        return self._doc

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def doc_len(self) -> int:
        return self._doc_len

    @property
    def positions(self) -> list:
        return self._positions

    @weight.setter
    def weight(self, new_weight:float) -> None:
        self._weight = new_weight

    def add_position(self, index:int) -> None:
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
                return f"{self._doc},{self._doc_len}:{self._weight:.2f}:{','.join([str(p) for p in self._positions])}"

            return f"{self._doc},{self._doc_len}:{self._weight:.2f}"

        if len(self._positions) > 0:
            return f"{self._doc}:{self._weight:.2f}:{','.join([str(p) for p in self._positions])}"

        return f"{self._doc}:{self._weight:.2f}"

    def __str__(self):
        if self._doc_len > 0:
            if len(self._positions) > 0:
                return f"{self._doc},{self._doc_len}:{self._weight:.2f}:{','.join([str(p) for p in self._positions])}"

            return f"{self._doc},{self._doc_len}:{self._weight:.2f}"

        if len(self._positions) > 0:
            return f"{self._doc}:{self._weight:.2f}:{','.join([str(p) for p in self._positions])}"

        return f"{self._doc}:{self._weight:.2f}"
