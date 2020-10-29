
from Tokenizer import Tokenizer
from CorpusReader import CorpusReader


class Indexer:
	"""
	Class used by index the tokens.

	...

	Attributes
	----------
	corpus : CorpusReader
		the CorpusReader object
	tokenizer : Tokenizer
		The Tokenizer object.
	index : dict
		The indexed tokens.

	Methods
	-------
	index()
		Return the indexs.
	indexing()
		Index the tokens.
	"""
	def __init__(self, corpus:CorpusReader, tokenizer:Tokenizer):
		"""
		Parameters
		----------
		corpus: CorpusReader
			the CorpusReader object with the loaded file
		tokenizer : Tokenizer
			The tokenizer object that will tokenize the documents.
		"""
		self._corpus = corpus
		self._tokenizer = tokenizer
		self._index = {}

	@property
	def index(self) -> dict:
		"""
		Returns
		-------
		dict
			A dict with indexed tokens.
		"""
		return self._index

	def indexing(self) -> None:
		"""Index the tokens, by processing 1000 documents at a time, tokenizing these documents and then indexing all"""
		# sort first by token and then by document Id
		while True:
			all_files, reached_end = self._corpus.process(1000)
			for doc_id, data in all_files.items():
				for token in self._tokenizer.tokenize(data):
					self._index[token] = self._index.get(token, set())
					self._index[token].add(doc_id)
			all_files.clear()
			if reached_end:
				break
