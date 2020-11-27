from collections import Counter
from math import sqrt

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
            self._query_vector[token] = weight / sqrt(weight_total)

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
        for token in self._tokenizer.tokenize(self._query):
            for token_info in self._index.get_token_search(token):
                doc = token_info.doc
                if doc not in prox_by_doc:
                    prox_by_doc[doc] = 0
                prox_by_doc[doc] += token_info.weight

        return sorted(prox_by_doc.items(), key=lambda t: t[1], reverse=True)
