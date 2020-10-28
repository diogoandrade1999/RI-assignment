import abc
import re
import json

from CorpusReader import CorpusReader
from nltk.stem.snowball import SnowballStemmer


class Tokenizer(metaclass=abc.ABCMeta):
	"""
	Abstract class used by tokenize the data.

	...

	Abstract methods
	-------
	tokenize()
		Tokenize the data.
	"""
	
	@abc.abstractmethod
	def tokenize(self) -> list:
		"""Tokenize the data."""
		pass


class SimpleTokenizer(Tokenizer):
	"""
	Class used by tokenize the data with a simple tokenizer.

	...

	Attributes
	----------
	corpus : CorpusReader
		The CorpusReader object.
	tokens : list
		The tokenized data.

	Methods
	-------
	tokens()
		Return the tokens.
	tokenize()
		Tokenize the data.
	"""

	def tokenize(self, data) -> list:
		"""Tokenize the data."""
		# replaces all non-alphabetic characters by a space
		tokens = re.sub('[^a-zA-Z]+', ' ', data)
		# put token in lowercase
		tokens = tokens.lower()
		# ignores all tokens with less than 3 characters
		return [token for token in tokens.split() if len(token) >= 3]


class ImprovedTokenizer(Tokenizer):
	"""
	Class used by tokenize the data with a improved tokenizer.

	...

	Attributes
	----------
	corpus : CorpusReader
		The CorpusReader object.
	tokens : list
		The tokenized data.
	stemmer : SnowballStemmer
		The stemmer object.

	Methods
	-------
	tokens()
		Return the tokens.
	tokenize()
		Tokenize the data.
	"""
	def __init__(self):
		with open("stopwords.json", "r") as stop:
			self._stopwords = set(json.load(stop))
		self._stemmer = SnowballStemmer("english")


	def tokenize(self, data) -> list:
		"""Tokenize the data."""
		# replaces all non-alphabetic by a space, and keep numbers and hyphens
		tokens = re.sub('[^a-zA-Z0-9\-]+', ' ', data)
		# put token in lowercase
		tokens = tokens.lower()
		# use stemmer
		return [self._stemmer.stem(token)
				for token in list(set(tokens.split())) if token not in self._stopwords]
