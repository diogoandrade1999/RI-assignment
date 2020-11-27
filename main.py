# Diogo Andrade 89265 MEI
# Pedro Oliveira 89156 MEI

import argparse
import logging
import time
import sys
import psutil
import os
from math import log2

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


def metrics(query_reader:QueryReader, indexer:Indexer, tokenizer:Tokenizer, use_bm:bool) -> dict:
    """
    Calculation of metrics.
    """
    results = {}
    for query_number, query in query_reader.queries.items():
        results[query_number] = {}
        
        start_time = time.time()

        query_search = Query(query, indexer, tokenizer)

        if use_bm:
            docs = query_search.lookup_bm25()
        else:
            docs = query_search.lookup_idf()

        results[query_number]['latency'] = time.time() - start_time

        docs_relevance = query_reader.queries_relevance[query_number][0].union(
                            query_reader.queries_relevance[query_number][1]).union(
                                query_reader.queries_relevance[query_number][2]
                            )
        docs_retrieved_total = [doc_id for doc_id, weigth in docs]

        for num_docs_retrieved in [10, 20, 50]:
            docs_retrieved = set(list(docs_retrieved_total)[:num_docs_retrieved])

            docs_relevance_retrieved = docs_retrieved & docs_relevance

            num_docs_relevance = len(docs_relevance)

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

                docs_precision = 0
                dcg = 0
                for i in range(len(docs_retrieved)):
                    k = i + 1
                    docs_retrieved_ap = set(list(docs_retrieved)[:k])
                    docs_relevance_retrieved_ap = docs_retrieved_ap & docs_relevance
                    docs_precision += len(docs_relevance_retrieved_ap) / k
                    if i == 0: 
                        dcg = query_reader.get_rank_value(query_number, docs_retrieved_total[i])
                        continue
                    dcg += query_reader.get_rank_value(query_number, docs_retrieved_total[i])/log2(k)
                average_precision = docs_precision / num_docs_relevance
                perfect_rank = query_reader.get_perfect_dcg(query_number, num_docs_retrieved)
                if perfect_rank != 0: ndcg = dcg/query_reader.get_perfect_dcg(query_number, num_docs_retrieved)
                else: ndcg = 0  
                results[query_number][num_docs_retrieved] = (precision, recall, f_measure, average_precision, ndcg)
    return results


def print_metrics(results:dict) -> None:
    """
    Print the metrics.
    """
    logger.info('   # %29s %29s %29s %29s %29s  Latency' % ('Precision', 'Recall', 'F-measure', 'Average Precision', 'NDCG'))
    logger.info('   %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s %9s' % \
        ('@10', '@20', '@50', '@10', '@20', '@50', '@10', '@20', '@50', '@10', '@20', '@50', '@10', '@20', '@50'))

    precision1_total = 0
    recall1_total = 0
    f_measure1_total = 0
    average_precision1_total = 0
    ndcg1_total = 0
    precision2_total = 0
    recall2_total = 0
    f_measure2_total = 0
    average_precision2_total = 0
    ndcg2_total = 0
    precision3_total = 0
    recall3_total = 0
    f_measure3_total = 0
    average_precision3_total = 0
    ndcg3_total = 0
    latency_total = []

    for query_number, x in results.items():
        precision1, recall1, f_measure1, average_precision1, ndcg1 = x[10]
        precision2, recall2, f_measure2, average_precision2, ndcg2 = x[20]
        precision3, recall3, f_measure3, average_precision3, ndcg3 = x[50]
        latency = x['latency']

        precision1_total += precision1
        recall1_total += recall1
        f_measure1_total += f_measure1
        average_precision1_total += average_precision1
        ndcg1_total += ndcg1
        precision2_total += precision2
        recall2_total += recall2
        f_measure2_total += f_measure2
        average_precision2_total += average_precision2
        ndcg2_total += ndcg2
        precision3_total += precision3
        recall3_total += recall3
        f_measure3_total += f_measure3
        average_precision3_total += average_precision3
        ndcg3_total += ndcg3
        latency_total.append(latency)

        logger.info('%4s %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f' % \
            (query_number,
            precision1, precision2, precision3,
            recall1, recall2, recall3,
            f_measure1, f_measure2, f_measure3,
            average_precision1, average_precision2, average_precision3,
            ndcg1, ndcg2, ndcg3,
            latency))

    latency_total = sorted(latency_total)

    logger.info('mean %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f %9f' % \
            (precision1_total / 50, precision2_total / 50, precision3_total / 50,
            recall1_total / 50, recall2_total / 50, recall3_total / 50,
            f_measure1_total / 50, f_measure2_total / 50, f_measure3_total / 50,
            average_precision1_total / 50, average_precision2_total / 50, average_precision3_total / 50,
            ndcg1_total / 50, ndcg2_total / 50, ndcg3_total / 50,
            latency_total[23] + latency_total[24]))
    logger.info('Query throughput: %9f', 50/sum(latency_total))


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
    print_metrics(metrics(query_reader, indexer, tokenizer, use_bm))


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
