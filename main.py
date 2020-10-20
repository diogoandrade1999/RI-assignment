# Diogo Andrade 89265 MEI
# Pedro Oliveira 89156 MEI

import argparse
import logging
import csv
import re
import time
import sys
from Tokenizer import SimpleTokenizer, ImprovedTokenizer
from Indexer import Indexer


logging.basicConfig(
    level=logging.INFO, format="%(message)s"
)

logger = logging.getLogger("main")


def questions(indexs):
    logger.info("Collection memory size: %s bytes" % sys.getsizeof(indexs))

    logger.info("Vocabulary size: %s tokens" % len(indexs))

    data = []
    for token in indexs:
        if len(indexs[token]) == 1:
            data += [token]
        # only want first ten
        if len(data) == 10:
            break

    logger.info('List the ten first terms (in alphabetic order) that appear in only one document:\n%s' % str(data))

    data = [k for k, v in sorted(indexs.items(), key = lambda x: len(x[1]))[-10:]]
    logger.info('List the ten terms with highest document frequency:\n%s' % str(data))


def simple_tokenizer(token, document):
    # replaces all non-alphabetic characters by a space
    token = re.sub('[^a-zA-Z]+', ' ', token)
    # put token in lowercase
    token = token.lower()
    # splits on whitespace
    tokens = token.split(' ')
    # ignores all tokens with less than 3 characters
    tokens = [(token, document) for token in tokens if len(token) >= 3]
    return tokens


def improved_tokenizer(token, document):
    pass


def tokenizing(data):
    tokens = []
    document_id = 0
    for document in data:
        # Ignore header
        if document_id != 0:
            if document[7] != '':
                if not args.tokenizing:
                    tokens += simple_tokenizer(document[2], document_id)
                    tokens += simple_tokenizer(document[7], document_id)
                else:
                    tokens += improved_tokenizer(document[2], document_id)
                    tokens += improved_tokenizer(document[7], document_id)
        document_id += 1
    return tokens

def main(file, tokenizing):
    try:

        # start tokenizing
        start_time = time.time()
        tokenizer = None
        if tokenizing:
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
        #questions(indexs)
    except FileNotFoundError as e:
        logger.warn("File not found!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="filename", required=True, help="Name of data file", metavar="FILE")
    parser.add_argument("-t", dest="tokenizing", required=False, help="Use improved tokenizer", default=False, action='store_true')
    args = parser.parse_args()

    main(args.filename, args.tokenizing)
