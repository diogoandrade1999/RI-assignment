
from Tokenizer import Tokenizer
from CorpusReader import CorpusReader
from TokenInfo import TokenInfo
from math import log10


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
		"""
		Index the tokens, by processing 1000 documents at a time,
		tokenizing these coduments and then indexing all.
		"""
		while True:
			all_files, reached_end = self._corpus.process(1000)

			for doc_id, data in all_files.items():
				for token, freq in self._tokenizer.tokenize(data):
					self._index[token] = self._index.get(token, set())
					self._index[token].add(TokenInfo(doc_id, freq))

			if reached_end:
				break
	
	def process_weights(self) -> None:
		"If the indexing is completed, it is possible to attribute the tf_idf to each token"
		
		if len(self._index) == 0:
			print("You have not processed any documents")
			return 
		
		for token in self._index:
			for info in self._index[token]:
				tf = 1 + log10(info.weight)
				idf = log10(self._corpus.number_of_read_docs/len(self._index[token]))
				info.weight = tf*idf
		
		count = 0
		for token in self._index:
			print(token, ":", self._index[token])
			count += 1
			if count > 5: return
