# Diogo Andrade 89265 MEI
# Pedro Oliveira 89156 MEI

import argparse
import logging
import time
import sys
from Tokenizer import SimpleTokenizer, ImprovedTokenizer
from Indexer import Indexer


logging.basicConfig(
    level=logging.INFO, format="%(message)s"
)

logger = logging.getLogger("main")


def questions(indexs):
    logger.info("Collection memory size: %s bytes" % sys.getsizeof(indexs.index))

    logger.info("Vocabulary size: %s tokens" % len(indexs.index))

    data = []
    for token, docs_id in indexs.index.items():
        if len(docs_id) == 1:
            data += [token]
        # only want first ten
        if len(data) == 10:
            break

    logger.info('List the ten first terms (in alphabetic order) that appear in only one document:\n%s' % str(data))

    data = [k for k, v in sorted(indexs.index.items(), key = lambda x: len(x[1]))[-10:]]
    logger.info('List the ten terms with highest document frequency:\n%s' % str(data))


def main(file, tokenizing):
    try:
        # start tokenizing
        start_time = time.time()
        if not tokenizing:
            tokenizer = SimpleTokenizer(file)
        else:
            tokenizer = ImprovedTokenizer(file)
        tokenizer.tokenize()
        logger.info("Tokenizing Time: %s seconds" % (time.time() - start_time))

        # start indexing
        start_time = time.time()
        indexs = Indexer(tokenizer)
        indexs.indexing()
        logger.info("Indexing Time: %s seconds" % (time.time() - start_time))   

        # assignment questions
        questions(indexs)
    except FileNotFoundError as e:
        logger.warning("File not found!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="filename", required=True, help="Name of data file", metavar="FILE")
    parser.add_argument("-t", dest="tokenizing", required=False, help="Use improved tokenizer", default=False, action='store_true')
    args = parser.parse_args()

    main(args.filename, args.tokenizing)
