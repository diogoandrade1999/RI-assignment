import xml.etree.ElementTree as ET
from math import log2


class QueryReader:
    """
    Class used to read queries.

    ...

    Attributes
    ----------
    queries : dict
        The list of queries.
    queries_relevance : dict
        The list of relevant queries.

    Methods
    -------
    _read_queries_xml()
        Read the file with the list of queries. File format xml.
    _read_queries_txt()
        Read the file with the list of queries. File format txt.
    _read_queries_relevance()
        Read the file with the list of relevant queries.
    get_perfect_dcg()
        Get the perfect dcg.
    get_rank_value()
        Get the doc rank value on query.
    """
    def __init__(self, query_file_path:str, query_relevance_file_path):
        """
        Parameters
        ----------
        query_file_path : str
            The query file path.
        query_relevance_file_path : str
            The query relevance file path.
        """
        self._query_file_path = query_file_path
        self._query_relevance_file_path = query_relevance_file_path
        if self._query_file_path[-4:] == '.xml':
            self._read_queries_xml()
        else:
            self._read_queries_txt()
        self._read_queries_relevance()

    @property
    def queries(self) -> dict:
        return self._queries

    @property
    def queries_relevance(self) -> dict:
        return self._queries_relevance

    def _read_queries_xml(self) -> None:
        """Read the file with the list of queries. File format xml."""
        self._queries = {}
        topics = ET.parse(self._query_file_path).getroot()
        for topic in topics:
            self._queries[topic.attrib['number']] = topic[0].text

    def _read_queries_txt(self) -> None:
        """Read the file with the list of queries. File format txt."""
        self._queries = {}
        with open(self._query_file_path, "r") as queries:
            for query_id, query in enumerate(queries, start=1):
                self._queries[str(query_id)] = query.rstrip()

    def _read_queries_relevance(self):
        """Read the file with the list of relevant queries."""
        self._queries_relevance = {}
        with open(self._query_relevance_file_path, "r") as queries:
            for query in queries:
                query_id, cord_ui, relevance = query.rstrip().split(' ')
                self._queries_relevance[query_id] = self._queries_relevance.get(query_id, {0: set(), 1: set(), 2: set()})
                self._queries_relevance[query_id][int(relevance)].add(cord_ui)

    def get_perfect_dcg(self, query_id, num_docs) -> float:
        """
        Get the perfect dcg.

        Returns
        -------
        float
            The perfect dcg.
        """
        perfect_rank = 0
        num_sums = 0
        for i in range(2,0,-1):
            perfect_docs = self._queries_relevance[query_id][i]
            for doc in perfect_docs:
                num_sums += 1
                if num_sums == 1: 
                    perfect_rank = i
                    continue
                perfect_rank += i / log2(num_sums)
                if num_sums == num_docs: return perfect_rank
        return perfect_rank

    def get_rank_value(self, query_id, doc) -> int:
        """
        Get the doc rank value on query.

        Returns
        -------
        int
            The rank.
        """
        if doc in self._queries_relevance[query_id][2]: return 2
        if doc in self._queries_relevance[query_id][1]: return 1
        return 0
