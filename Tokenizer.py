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
	tokens()
		Return the tokens.
	tokenize()
		Tokenize the data.
	"""
	@property
	@abc.abstractmethod
	def tokens(self) -> list:
		"""
		Returns
		-------
		list
			A list with tokenized data.
		"""
		pass
	
	@abc.abstractmethod
	def tokenize(self) -> None:
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
	def __init__(self, data_file_path:str):
		"""
		Parameters
		----------
		data_file_path : str
			The data file path.
		"""
		self._corpus = CorpusReader(data_file_path)
		self._tokens = []

	@property
	def tokens(self) -> list:
		"""
		Returns
		-------
		list
			A list with tokenized data.
		"""
		return self._tokens

	def tokenize(self) -> None:
		"""Tokenize the data."""
		processed_files = self._corpus.process()
		for doc_id, data in processed_files.items():
			# replaces all non-alphabetic characters by a space
			tokens = re.sub('[^a-zA-Z]+', ' ', data)
			# put token in lowercase
			tokens = tokens.lower()
			# ignores all tokens with less than 3 characters
			self._tokens += [(token, doc_id) for token in tokens.split() if len(token) >= 3]


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
	def __init__(self, data_file_path:str):
		"""
		Parameters
		----------
		data_file_path : str
			The data file path.
		"""
		self._corpus = CorpusReader(data_file_path)
		self._tokens = []
		with open("stopwords.json", "r") as stop:
			self._stopwords = set(json.load(stop))
		self._stemmer = SnowballStemmer("english")

	@property
	def tokens(self) -> list:
		"""
		Returns
		-------
		list
			A list with tokenized data.
		"""
		return self._tokens

	def tokenize(self) -> None:
		"""Tokenize the data."""
		processed_files = self._corpus.process()
		for file_id, doc in processed_files.items():
			# replaces all non-alphabetic or numeric or hyphen characters by a space
			tokens = re.sub('[^a-zA-Z0-9\-/]+', ' ', doc)
			# put token in lowercase
			tokens = tokens.lower()
			# use stemmer
			self._tokens += [(self._stemmer.stem(token), file_id)
							 for token in list(set(tokens.split())) if token not in self._stopwords]
