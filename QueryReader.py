import xml.etree.ElementTree as ET


class QueryReader:
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
        self._queries = {}
        topics = ET.parse(self._query_file_path).getroot()
        for topic in topics:
            self._queries[topic.attrib['number']] = topic[0].text

    def _read_queries_txt(self) -> None:
        self._queries = {}
        with open(self._query_file_path, "r") as queries:
            for query_id, query in enumerate(queries, start=1):
                self._queries[str(query_id)] = query.rstrip()

    def _read_queries_relevance(self):
        self._queries_relevance = {}
        with open(self._query_relevance_file_path, "r") as queries:
            for query in queries:
                query_id, cord_ui, relevance = query.rstrip().split(' ')
                self._queries_relevance[query_id] = self._queries_relevance.get(query_id, {'0': [], '1': [], '2': []})
                self._queries_relevance[query_id][relevance] += [cord_ui]
