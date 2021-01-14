from collections import Counter
from math import sqrt
from itertools import combinations

from Tokenizer import Tokenizer
from Indexer import Indexer


class Query:
    """
    Class used to search the relevant tokens of queries.

    ...

    Methods
    -------
    __process()
        Calculates the weight of the query tokens in case of using the idf.
    lookup_idf()
        Search the tokens relevant for the query. Using idf.
    lookup_bm25()
        Search the tokens relevant for the query. Using bm25.
    """
    def __init__(self, query:str, index:Indexer, tokenizer:Tokenizer):
        """
        Parameters
        ----------
        query : str
            The query file path.
        index : Indexer
            The indexer object.
        tokenizer : Tokenizer
            The tokenizer object that will tokenize the documents.
        """
        self._query = query
        self._tokenizer = tokenizer
        self._index = index
        self._query_vector = {}

    def __process(self) -> None:
        """
        Calculates the weight of the query tokens in case of using the idf.
        """
        # * First step, tokenize the query and get the weights
        weight_total = 0
        token_list = self._tokenizer.tokenize(self._query)
        token_list = dict(Counter(token_list)).items()
        for token, freq in token_list:
            weight = freq * self._index.get_token_freq(token)
            self._query_vector[token] = weight
            weight_total += weight ** 2

        for token in self._query_vector:
            self._query_vector[token] = self._query_vector[token] / sqrt(weight_total)

    def lookup_idf(self) -> list:
        """
        Search the tokens relevant for the query. Using idf.

        Returns
        -------
        list
            The list of relevant tokens.
        """
        self.__process()
        prox_by_doc = {}

        if 'POSITIONS' in str(self._index):
            tokens_info = {}
            for token in self._query_vector:
                tokens_info[token] = {}
                for token_info in self._index.get_token_search(token):
                    tokens_info[token][token_info.doc] = (token_info.weight, token_info.positions)

            docs_boost = self._boost(tokens_info)

            for token in tokens_info:
                for doc, (weight, positions) in tokens_info[token].items():
                    if doc not in prox_by_doc:
                        prox_by_doc[doc] = 0
                    prox_by_doc[doc] += self._query_vector[token] * weight
        else:
            for token in self._query_vector:
                for token_info in self._index.get_token_search(token):
                    doc = token_info.doc
                    if doc not in prox_by_doc:
                        prox_by_doc[doc] = 0
                    prox_by_doc[doc] += self._query_vector[token] * token_info.weight

        return sorted(prox_by_doc.items(), key=lambda t: t[1], reverse=True)

    def lookup_bm25(self) -> list:
        """
        Search the tokens relevant for the query. Using bm25.

        Returns
        -------
        list
            The list of relevant tokens.
        """
        prox_by_doc = {}

        if 'POSITIONS' in str(self._index):
            tokens_info = {}
            for token in self._tokenizer.tokenize(self._query):
                tokens_info[token] = {}
                for token_info in self._index.get_token_search(token):
                    tokens_info[token][token_info.doc] = (token_info.weight, token_info.positions)

            docs_boost = self._boost(tokens_info)

            for token in tokens_info:
                for doc, (weight, positions) in tokens_info[token].items():
                    if doc not in prox_by_doc:
                        prox_by_doc[doc] = 0
                    prox_by_doc[doc] += weight
        else:
            for token in self._tokenizer.tokenize(self._query):
                for token_info in self._index.get_token_search(token):
                    doc = token_info.doc
                    if doc not in prox_by_doc:
                        prox_by_doc[doc] = 0
                    prox_by_doc[doc] += token_info.weight

        return sorted(prox_by_doc.items(), key=lambda t: t[1], reverse=True)

    def _boost(self, tokens_info, token_range=50):
        docs_boost = {}
        tokens = tokens_info.keys()
        if len(tokens) > 1:
            for (t1, t2) in combinations(tokens, 2):
                docs = set(tokens_info[t1].keys()).intersection(set(tokens_info[t2].keys()))

                for doc in docs:
                    docs_boost[doc] = docs_boost.get(doc, 0)

                    weight1 = tokens_info[t1][doc][0]
                    positions1 = tokens_info[t1][doc][1]

                    weight2 = tokens_info[t2][doc][0]
                    positions2 = tokens_info[t2][doc][1]

                    for p1 in positions1:
                        for p2 in positions2:
                            if p1 in range(p2, p2 + token_range) or p1 in range(p2 - token_range, p2):
                                docs_boost[doc] += weight1 * weight2
        return docs_boost
