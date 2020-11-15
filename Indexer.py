
from Tokenizer import Tokenizer
from CorpusReader import CorpusReader
from TokenInfo import TokenInfo
from math import log10, sqrt


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
				doc_weight = 0
				token_list = self._tokenizer.tokenize(data)
				for token, freq in token_list:
					tf = 1 + log10(freq)
					self._index[token] = self._index.get(token, [])
					self._index[token].append(TokenInfo(doc_id, tf))
					doc_weight += tf**2
				
				for token, freq in token_list:
					self._index[token][-1].weight = self._index[token][-1].weight/sqrt(doc_weight)

			if reached_end:
				break
	
	def process_weights(self) -> None:
		"If the indexing is completed, it is possible to attribute the tf_idf to each token with the lnc method"
		
		if len(self._index) == 0:
			print("You have not processed any documents")
			return 
		
		weight_by_doc = {}

		for token in self._index:
			for info in self._index[token]:
				tf = 1 + log10(info.weight) ## logarithmic count
				idf = 1 #number	
				info.weight = tf*idf
				if info.doc not in weight_by_doc:
					weight_by_doc[info.doc] += 0

	def get_token_search(self, token):
		return self._index.get(token, [])

	def get_token_freq(self, token):
		if token not in self._index:
			return 0
		
		return log10(self._corpus.number_of_read_docs/len(self._index[token]))
