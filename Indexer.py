class Indexer:
	def __init__(self, tokenizer):
		self.tokenizer = tokenizer
		self.index = {}

	def indexing(self):
		# sort first by token and then by document Id
		self.tokenizer.tokens.sort(key=lambda x: (x[0], x[1]))
		for token, doc_id in self.tokenizer.tokens:
			if token not in self.index:
				self.index[token] = set()
			self.index[token].add(doc_id)