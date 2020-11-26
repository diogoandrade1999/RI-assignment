# Diogo Andrade 89265 MEI
# Pedro Oliveira 89156 MEI

import argparse
import logging
import time
import sys
import psutil
import os

from Tokenizer import Tokenizer, SimpleTokenizer, ImprovedTokenizer
from Indexer import Indexer, IndexerBM25
from CorpusReader import CorpusReader
from QueryReader import QueryReader
from Query import Query


logging.basicConfig(
    level=logging.INFO, format="%(message)s"
)

logger = logging.getLogger("main")


def questions(indexer:Indexer) -> None:
    """
    Print the answers of this assignment.
    """
    process = psutil.Process(os.getpid())
    logger.info("Collection memory size: %s bytes" % process.memory_info().rss)

    logger.info("Vocabulary size: %s tokens" % len(indexer.index))

    data = []
    for token in sorted(indexer.index.keys()):
        if len(indexer.index[token]) == 1:
            data += [token]
        # only want first ten
        if len(data) == 10:
            break

    logger.info('List the ten first terms (in alphabetic order) that appear in only one document:\n%s' % str(data))

    data = [k for k, v in sorted(indexer.index.items(), key = lambda x: len(x[1]))[-10:]]
    logger.info('List the ten terms with highest document frequency:\n%s' % str(data))


def metrics(query_reader:QueryReader, indexer:Indexer, tokenizer:Tokenizer, use_bm:bool) -> None:
    results = {}
    for query_number, query in query_reader.queries.items():
        start_time = time.time()

        query_search = Query(query, indexer, tokenizer)

        if use_bm:
            docs = query_search.lookup_bm25()
        else:
            docs = query_search.lookup_idf()
        
        latency = time.time() - start_time

        docs_relevance = query_reader.queries_relevance[query_number][1].union(
                            query_reader.queries_relevance[query_number][2])
        docs_retrieved = set(docs.keys())

        results[query_number] = {}
        results[query_number]['latency'] = latency
        for x in [10, 20, 50]:
            docs_retrieved = set(list(docs_retrieved)[:x])

            docs_relevance_retrieved = docs_retrieved & docs_relevance

            num_docs_relevance = len(docs_relevance)
            num_docs_retrieved = len(docs_retrieved)
            num_docs_relevance_retrieved = len(docs_relevance_retrieved)

            precision = 0
            recall = 0
            f_measure = 0
            average_precision = 0
            ndcg = 0

            if num_docs_relevance_retrieved != 0:
                if num_docs_retrieved != 0:
                    precision = num_docs_relevance_retrieved / num_docs_retrieved

                if num_docs_relevance != 0:
                    recall = num_docs_relevance_retrieved / num_docs_relevance

                if (precision + recall) != 0:
                    f_measure = (2 * precision * recall) / (precision + recall)

                # está mal
                docs_precision = [docs[doc] for doc in docs_relevance_retrieved]
                average_precision = sum(docs_precision) / num_docs_relevance_retrieved

                dcg = 0
            results[query_number][x] = (precision, recall, f_measure, average_precision, ndcg)

    logger.info(' # %25s %25s %25s %30s %25s %25s' % ('Precision', 'Recall', 'F-measure', 'Average Precision', 'NDCG', 'Latency'))
    logger.info('   %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s' % \
        ('@10', '@20', '@30', '@10', '@20', '@30', '@10', '@20', '@30', '@10', '@20', '@30', '@10', '@20', '@30'))
    for query_number, x in results.items():
        precision1, recall1, f_measure1, average_precision1, ndcg1 = x[10]
        precision2, recall2, f_measure2, average_precision2, ndcg2 = x[20]
        precision3, recall3, f_measure3, average_precision3, ndcg3 = x[50]
        latency = x['latency']
        logger.info('%2s %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f' % \
            (query_number,
            precision1, precision2, precision3,
            recall1, recall2, recall3,
            f_measure1, f_measure2, f_measure3,
            average_precision1, average_precision2, average_precision3,
            ndcg1, ndcg2, ndcg3,
            latency))


def main(
    data_file_path:str,
    improved_tokenizer:bool,
    file_to_write:str,
    use_bm:bool,
    bm_k1:float,
    bm_b:float,
    query_file_path:str,
    query_relevance_file_path:str
    ) -> None:
    # read data file
    corpus = CorpusReader(data_file_path)

    # read queries
    query_reader = QueryReader(query_file_path, query_relevance_file_path)
 
    # create tokenizer
    if not improved_tokenizer:
        tokenizer = SimpleTokenizer()
    else:
        tokenizer = ImprovedTokenizer()

    # create indexer
    if use_bm:
        indexer = IndexerBM25(corpus, tokenizer, bm_k1, bm_b)
    else:
        indexer = Indexer(corpus, tokenizer)   

    # start indexing
    start_time = time.time()
    indexer.indexing()
    logger.info("Indexing Time: %s seconds" % (time.time() - start_time))   

    # assignment questions
    # questions(indexer)

    # write index
    if file_to_write: 
        start_time = time.time()
        indexer.write(file_to_write)
        logger.info("Writing Time: %s seconds" % (time.time() - start_time))   

    # metrics
    metrics(query_reader, indexer, tokenizer, use_bm)


if __name__ == "__main__":
    """
    EXECUTION
    ---------
    simple tokenizer:
        python3 main.py -f data.csv
    improved tokenizer:
        python3 main.py -f data.csv -t
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="data_file_path", required=True, help="Data file path")
    parser.add_argument("-t", dest="improved_tokenizer", required=False, help="Use improved tokenizer", default=False, action='store_true')
    parser.add_argument("-w", dest="indexer_file", required=False, help="Write index to file", default=None)
    parser.add_argument("-b", dest="bm25", required=False, help="Use the BM25 method to rank", default=False, action='store_true')
    parser.add_argument("--bk1", dest="bm25_k1_value", required=False, help="K value for the BM25 method", type=float, default=1.2)
    parser.add_argument("--bb", dest="bm25_b_value", required=False, help="B value for the BM25 method", type=float, default=0.75)  
    parser.add_argument("-q", dest="query_file_path", required=True, help="Queries file path")
    parser.add_argument("-qr", dest="query_relevance_file_path", required=True, help="Queries relevance file path")
    args = parser.parse_args()

    if not args.bm25 and (args.bm25_k1_value != 1.2 or args.bm25_b_value != 0.75):
        parser.error("--bk1 and --bb requires the flag -b")
    elif args.bm25_k1_value != 1.2 and not (1 < args.bm25_k1_value < 2):
        parser.error("K value for the BM25 method must be greater than 1 and less than 2")
    elif args.bm25_b_value != 0.75 and not (0 < args.bm25_b_value < 1):
        parser.error("B value for the BM25 method must be greater than 0 and less than 1")

    main(args.data_file_path,
         args.improved_tokenizer,
         args.indexer_file, 
         args.bm25,
         args.bm25_b_value,
         args.bm25_k1_value,
         args.query_file_path,
         args.query_relevance_file_path)
