
class Indexer:
	def __init__(self, tokenizer):
		self._tokenizer = tokenizer
		self._index = {}

	@property
	def index(self):
		return self._index

	def indexing(self):
		# sort first by token and then by document Id
		self._tokenizer.tokens.sort(key=lambda x: (x[0], x[1]))
		for token, doc_id in self._tokenizer.tokens:
			if token not in self._index:
				self._index[token] = set()
			self._index[token].add(doc_id)
		i = 0
		for token in self._index:
			print(token, self._index[token])
			i+=1
			if i > 20: break
