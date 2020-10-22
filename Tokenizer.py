import abc
import logging
import re
from CorpusReader import CorpusReader
import json


class Tokenizer(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def tokenize(self):
		pass


class SimpleTokenizer(Tokenizer):
	def __init__(self, file):
		self.corpus = CorpusReader(file)
		self.tokens = []

	def tokenize(self):
		processed_files = self.corpus.process()
		for file_id, doc in processed_files.items():
			# replaces all non-alphabetic characters by a space
			tokens = re.sub('[^a-zA-Z]+', ' ', doc[0] + doc[1])
			# put token in lowercase
			tokens = tokens.lower()
			# ignores all tokens with less than 3 characters
			self.tokens += [(token, file_id) for token in tokens.split() if len(token) >= 3]


class ImprovedTokenizer(Tokenizer):
	def __init__(self, file):
		self.corpus = CorpusReader(file)
		self.tokens = []
		with open("stopwords.json", "r") as stop:
			self.stopwords = json.load(stop)

	def tokenize(self):
		processed_files = self.corpus.process()
		for file_id, doc in processed_files.items():
			# replaces all non-alphabetic characters by a space
			tokens = re.sub('[^a-zA-Z]+', ' ', doc[0] + doc[1])
			# put token in lowercase
			tokens = tokens.lower()
			# ignores all tokens with less than 3 characters
			self.tokens += [(token, file_id) for token in tokens.split() if token not in self.stopwords]

