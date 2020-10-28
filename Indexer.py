
from Tokenizer import Tokenizer


class Indexer:
	"""
	Class used by index the tokens.

	...

	Attributes
	----------
	tokenizer : Tokenizer
		The tokenizer object.
	index : dict
		The indexed tokens.

	Methods
	-------
	index()
		Return the indexs.
	indexing()
		Index the tokens.
	"""
	def __init__(self, tokenizer:Tokenizer):
		"""
		Parameters
		----------
		tokenizer : Tokenizer
			The tokenizer object.
		index : dict
			The indexed tokens.
		"""
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
		"""Index the tokens."""
		# sort first by token and then by document Id
		self._tokenizer.tokens.sort(key=lambda x: (x[0], x[1]))
		for token, doc_id in self._tokenizer.tokens:
			self._index[token] = self._index.get(token, set())
			self._index[token].add(doc_id)
