class TokenInfo:
    def __init__(self, doc, doc_freq):
        self._doc = doc
        self._weight = doc_freq
    
    @property
    def doc(self):
        return self._doc
    
    @property
    def weight(self):
        return self._weight 
    
    @weight.setter
    def weight(self, new_weight):
        self._weight = new_weight

    def __eq__(self, token):
        if token is None: return False

        if not isinstance(token, TokenInfo): return False

        return self._doc == token.doc

    def __hash__(self):
        return hash(self._doc)
    
    def __repr__(self):
        return f"({self._doc}, {self._weight:.2f})"

    def __str__(self):
        return f"({self._doc}, {self._weight:.2f})"