import abc
import re
from CorpusReader import CorpusReader
from nltk.stem import PorterStemmer
import json


class Tokenizer(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def tokenize(self):
		pass

	@property    
	@abc.abstractmethod
	def tokens(self):
		pass


class SimpleTokenizer(Tokenizer):
	def __init__(self, file):
		self._corpus = CorpusReader(file)
		self._tokens = []

	@property
	def tokens(self):
		return self._tokens

	def tokenize(self):
		processed_files = self._corpus.process()
		for doc_id, data in processed_files.items():
			# replaces all non-alphabetic characters by a space
			tokens = re.sub('[^a-zA-Z]+', ' ', data)
			# put token in lowercase
			tokens = tokens.lower()
			# ignores all tokens with less than 3 characters
			self._tokens += [(token, doc_id) for token in tokens.split() if len(token) >= 3]


class ImprovedTokenizer(Tokenizer):
	def __init__(self, file):
		self._corpus = CorpusReader(file)
		self._tokens = []
		with open("stopwords.json", "r") as stop:
			self._stopwords = json.load(stop)
		self._stemmer = PorterStemmer()

	@property
	def tokens(self):
		return self._tokens

	def tokenize(self):
		processed_files = self._corpus.process()
		for doc_id, data in processed_files.items():
			# replaces all non-alphabetic characters by a space
			tokens = re.sub('[^a-zA-Z]+', ' ', data)
			# put token in lowercase
			tokens = tokens.lower()
			# use Porter Stemmer
			self._tokens += [(self._stemmer.stem(token), doc_id)
							 for token in tokens.split() if token not in self._stopwords]
