# Diogo Andrade 89265 MEI
# Pedro Oliveira 89156 MEI

import argparse
import logging
import time
import sys
import psutil
import os

from Tokenizer import SimpleTokenizer, ImprovedTokenizer
from Indexer import Indexer


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
    for token, docs_id in indexer.index.items():
        if len(docs_id) == 1:
            data += [token]
        # only want first ten
        if len(data) == 10:
            break

    logger.info('List the ten first terms (in alphabetic order) that appear in only one document:\n%s' % str(data))

    data = [k for k, v in sorted(indexer.index.items(), key = lambda x: len(x[1]))[-10:]]
    logger.info('List the ten terms with highest document frequency:\n%s' % str(data))


def main(data_file_path:str, improved_tokenizer:bool) -> None:
    if not improved_tokenizer:
        tokenizer = SimpleTokenizer(data_file_path)
    else:
        tokenizer = ImprovedTokenizer(data_file_path)

    indexs = Indexer(tokenizer)

    # start tokenizing
    start_time = time.time()
    tokenizer.tokenize()
    logger.info("Tokenizing Time: %s seconds" % (time.time() - start_time))

    # start indexing
    start_time = time.time()
    indexs.indexing()
    logger.info("Indexing Time: %s seconds" % (time.time() - start_time))   

    # assignment questions
    questions(indexs)


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
    args = parser.parse_args()

    main(args.data_file_path, args.improved_tokenizer)
