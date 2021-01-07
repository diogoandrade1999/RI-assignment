from collections import Counter
from math import log10, sqrt

from Tokenizer import Tokenizer
from CorpusReader import CorpusReader
from TokenInfo import TokenInfo


class Indexer:
	"""
	Class used by index the tokens.

	...

	Attributes
	----------
	index : dict
		The indexed tokens.

	Methods
	-------
	indexing()
		Index the tokens.
	get_token_search()
		Search for the token on indexs.
	get_token_freq()
		Get the token fregquency.
	write()
		Write the indexs on file.
	"""
	def __init__(self, corpus:CorpusReader, tokenizer:Tokenizer):
		"""
		Parameters
		----------
		corpus: CorpusReader
			The CorpusReader object with the loaded file.
		tokenizer : Tokenizer
			The tokenizer object that will tokenize the documents.
		"""
		self._corpus = corpus
		self._tokenizer = tokenizer
		self._index = {}

	@property
	def index(self) -> dict:
		return self._index

	def indexing(self) -> None:
		"""
		Index the tokens, by processing 1000 documents at a time,
		tokenizing these coduments and then indexing all.
		"""
		while True:
			all_files, reached_end = self._corpus.process(1000)

			for doc_id, data in all_files.items():
				doc_weight = 0
				token_list = self._tokenizer.tokenize(data)
				token_list = dict(Counter(token_list))
				for token, freq in token_list.items():
					tf = 1 + log10(freq)
					self._index[token] = self._index.get(token, [])
					self._index[token].append(TokenInfo(doc_id, tf))
					doc_weight += tf ** 2
				
				for token in token_list:
					self._index[token][-1].weight = self._index[token][-1].weight / sqrt(doc_weight)

			if reached_end:
				break

	def get_token_search(self, token) -> list:
		"""
		Search for the token on indexs.

		Returns
		-------
		list
			The token list.
		"""
		return self._index.get(token, [])

	def get_token_freq(self, token) -> float:
		"""
		Get the token fregquency.

		Returns
		-------
		float
			The token frequency.
		"""
		if token not in self._index:
			return 0

		return log10(self._corpus.number_of_read_docs / len(self._index[token]))

	def write(self, file) -> None:
		"""Write the indexs on file."""
		with open(file, "w") as writer:
			for token in self._index:
				line = "{}:{:.3f}".format(token, self.get_token_freq(token))
				for info in self._index[token]:
					line += ";" + str(info)
				writer.write(line + "\n")


class IndexerBM25(Indexer):
	"""
	Class used by index the tokens.

	...

	Methods
	-------
	indexing()
		Index the tokens.
	"""
	def __init__(self, corpus:CorpusReader, tokenizer:Tokenizer, k1:float, b:float):
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
		self._k1 = k1
		self._b = b

	def indexing(self):
		"""
		Index the tokens, by processing 1000 documents at a time,
		tokenizing these coduments and then indexing all.
		"""
		doc_lens = {}
		avg_doc_len = 0	
		while True:
			all_files, reached_end = self._corpus.process(1000)
			for doc_id, data in all_files.items():
				token_list = self._tokenizer.tokenize(data)
				doc_lens[doc_id] = len(token_list)
				avg_doc_len += len(token_list)
				token_list = dict(Counter(token_list))
				for token, freq in token_list.items():
					self._index[token] = self._index.get(token, [])
					self._index[token].append(TokenInfo(doc_id, freq))

			if reached_end:
				break

		avg_doc_len /= self._corpus.number_of_read_docs

		for token in self._index:
			for info in self._index[token]:
				info.weight = self.get_token_freq(token) * (self._k1 + 1) * info.weight / \
				(self._k1 * ((1 - self._b) + self._b * doc_lens[info.doc] / avg_doc_len) + info.weight)
