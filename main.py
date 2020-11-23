# Diogo Andrade 89265 MEI
# Pedro Oliveira 89156 MEI

import argparse
import logging
import time
import sys
import psutil
import os

from Tokenizer import SimpleTokenizer, ImprovedTokenizer
from Indexer import Indexer, IndexerBM25
from CorpusReader import CorpusReader


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


def main(data_file_path:str, improved_tokenizer:bool, file_to_write:str, use_bm:bool, bm_k1:float, bm_b:float) -> None:
    corpus = CorpusReader(data_file_path)

    if not improved_tokenizer:
        tokenizer = SimpleTokenizer()
    else:
        tokenizer = ImprovedTokenizer()

    if use_bm:
        k1 = bm_k1 if bm_k1 and 1<bm_k1<2 else 1.2
        b = bm_b if bm_b and 0<bm_b<1 else 0.75
        indexs = IndexerBM25(corpus, tokenizer, k1, b)
    else:
        indexs = Indexer(corpus, tokenizer)

    # start indexing
    start_time = time.time()
    indexs.indexing()
    logger.info("Indexing Time: %s seconds" % (time.time() - start_time))   

    # assignment questions
    questions(indexs)

    #lookup times

    #write index
    if file_to_write: 
        start_time = time.time()
        indexs.write(file_to_write)
        logger.info("Writing Time: %s seconds" % (time.time() - start_time))   


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
    parser.add_argument("--bk1", dest="bm25_k1_value", required=False, help="K value for the BM25 method", type=float)
    parser.add_argument("--bb", dest="bm25_b_value", required=False, help="B value for the BM25 method", type=float)  

    args = parser.parse_args()

    err_message = """
    usage: main.py [-h] -f DATA_FILE_PATH [-t] [-w INDEXER_FILE] [-b BM25]
               [--bk1 BM25_K1_VALUE] [--bb BM25_B_VALUE]
    main.py: error: 
    """

    if args.bm25_b_value is not None and not args.bm25:
        print(err_message + "you must specify the bm25 option to introduce the b value")

    if args.bm25_k1_value is not None and not args.bm25:
        print(err_message + "you must specify the bm25 option to introduce the k1 value")

    main(args.data_file_path, args.improved_tokenizer, args.indexer_file, 
        args.bm25, args.bm25_b_value, args.bm25_k1_value)
