from collections import Counter
from math import log10, sqrt
import os

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
	def __init__(self, corpus:CorpusReader, tokenizer:Tokenizer, index_folder:str):
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
		self._index_folder = index_folder
		self._mem_limit = 8*1024*1024 #capping off at 8 MiB

	@property
	def index(self) -> dict:
		return self._index

	def indexing(self) -> None:
		"""
		Generic function that will build the index for the whole collection by calling the methods,
		or steps on by one
		"""
		print("Start spimi algorithm")
		self._spimi_build()

		print("Start merging")
		self._merge_docs()

		print("Calculating Weights")
		self._calculate_weights()
		
		print("Divide Documents")
		self._divide_docs()
		

	def _spimi_build(self) -> None:
		"""
		Index the tokens, by processing 1000 documents at a time,
		tokenizing these coduments and then indexing all.
		"""
		counter = 0
		filename = self._index_folder + "/index-part-"

		while True:
			all_files, reached_end = self._corpus.process(1000)
			self._index.clear()
			counter += 1

			for doc_id, data in all_files.items():
				token_list = self._tokenizer.tokenize(data)
				token_list = dict(Counter(token_list))
				doc_weight = 0
				for token, freq in token_list.items():
					tf = 1 + log10(freq)
					self._index[token] = self._index.get(token, [])
					self._index[token].append(TokenInfo(doc_id, freq))
					doc_weight += tf ** 2
				
				for token in token_list:
					self._index[token][-1].weight = self._index[token][-1].weight / sqrt(doc_weight)

			self.write(filename + str(counter) + ".txt")

			if reached_end:
				break

	def __parse_line(self, line:str) -> list:
		list_of_terms =  line.rstrip().split(";")

		return list_of_terms[0], ";".join(list_of_terms[1:])
	
	def _merge_docs(self) -> None:
		"""
		Merge the documents created by the indexer
		"""
		number_of_files = 5
		line_by_reader = {}	
		filename = self._index_folder + "/index-part-"
		onlyfiles = [self._index_folder + "/" + f for f in os.listdir(self._index_folder) if os.path.isfile(os.path.join(self._index_folder, f))]
		counter = len(onlyfiles)
		while len(onlyfiles) > 1:
			counter += 1

			# open writer pointers
			writer = open(filename + str(counter) + ".txt", "w")
			
			# open reader pointers
			for reader in onlyfiles[:number_of_files]:
				line_by_reader[reader] = [open(reader, "r"), "", "", True]
			
			while True:
				# advance needed pointers
				to_close = []
				for reader in line_by_reader:
					if line_by_reader[reader][-1]:
						line_by_reader[reader][-1] = False
						line = line_by_reader[reader][0].readline()

						# If it's an empty line, then it's ready to be removed from the dictionary
						if len(line) == 0:
							to_close.append(reader)
							continue

						line_by_reader[reader][1:3] = self.__parse_line(line)

				if len(to_close) > 0:
					for line in to_close: 
						line_by_reader[line][0].close()
						os.remove(line)
						line_by_reader.pop(line)
				
				# End condition is there are no open readers in the dictionary
				if len(line_by_reader) == 0: 
					break

				#Get smallest token
				smallest_token = min([line_by_reader[reader][1] for reader in line_by_reader])
	
				#Start building merged line
				line_to_write = smallest_token

				for reader in line_by_reader:
					if line_by_reader[reader][1] == smallest_token:
						line_by_reader[reader][-1] = True
						line_to_write += ";" + line_by_reader[reader][2]
				
				writer.write(line_to_write + "\n")

			writer.close()
				
			onlyfiles = [self._index_folder + "/" + f for f in os.listdir(self._index_folder) if os.path.isfile(os.path.join(self._index_folder, f))]
			
	def _calculate_weights(self) -> None:
		"""
		Rewrite the final index document to have the proper term weights according to the tf-idf
		"""
		onlyfiles = [self._index_folder + "/" + f for f in os.listdir(self._index_folder) if os.path.isfile(os.path.join(self._index_folder, f))][0]
		merged_index_reader = open(onlyfiles, "r")
		final_index_writer = open(self._index_folder + "/final-index.txt", "w")

		while True:
			term_line = merged_index_reader.readline()
			
			if term_line == "":
				break

			term_info = term_line.split(";")
			term = term_info.pop(0)
			
			term_freq = log10(self._corpus.number_of_read_docs / len(term_info))

			final_index_writer.write(f"{term}:{term_freq:.2f};" + ";".join(term_info))

		merged_index_reader.close()
		os.remove(onlyfiles)
		final_index_writer.close()
	
	def _divide_docs(self) -> None:
		"""
		Final component of the index building pipeline where we divide the final index document in various,
		smaller documents
		"""
		with open(self._index_folder + "/final-index.txt", "r") as index_reader:
			line_to_write = ""
			starter_token = ""
			while True:
				read_line = index_reader.readline()
				if read_line == "":
					filename = "/"+starter_token + ".txt"
					with open(self._index_folder + filename, "w") as writer:
						writer.write(line_to_write)
					break

				if len(starter_token) == 0:
					starter_token = read_line[:read_line.index(":")]
				
				line_to_write += read_line
				if len(line_to_write) > self._mem_limit:
					filename = "/"+starter_token + "-" +read_line[:read_line.index(":")] + ".txt"
					with open(self._index_folder + filename, "w") as writer:
						writer.write(line_to_write)
					line_to_write = ""
					starter_token = ""
			
		os.remove(self._index_folder + "/final-index.txt")
				

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
		Get the token frequency.

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
			for token in sorted(self._index.keys()):
				#line = "{}:{:.3f}".format(token, self.get_token_freq(token))
				line = "{}".format(token)
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
	def __init__(self, corpus:CorpusReader, tokenizer:Tokenizer, index_folder:str, k1:float, b:float):
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
		self._index_folder = index_folder
		self._k1 = k1
		self._b = b
		self._mem_limit = 8*1024*1024 #capping off at 8 MiB
		self._avg_doc_len = 0

	def _spimi_build(self):
		"""
		Index the tokens, by processing 1000 documents at a time,
		tokenizing these coduments and then indexing all.
		"""
		counter = 0
		filename = self._index_folder + "/index-part-"

		while True:
			all_files, reached_end = self._corpus.process(1000)
			self._index.clear()
			counter += 1
			
			for doc_id, data in all_files.items():
				token_list = self._tokenizer.tokenize(data)
				self._avg_doc_len += len(token_list)
				token_list = dict(Counter(token_list))
				for token, freq in token_list.items():
					self._index[token] = self._index.get(token, [])
					self._index[token].append(TokenInfo(doc_id, freq, len(token_list)))

			self.write(filename + str(counter) + ".txt")

			if reached_end:
				break

		
	def _calculate_weights(self):
		"""
		Rewrite the final index document to have the proper term weights with the BM25 algorithms
		"""

		self._avg_doc_len /= self._corpus.number_of_read_docs

		onlyfiles = [self._index_folder + "/" + f for f in os.listdir(self._index_folder) if os.path.isfile(os.path.join(self._index_folder, f))][0]
		merged_index_reader = open(onlyfiles, "r")
		final_index_writer = open(self._index_folder + "/final-index.txt", "w")

		while True:
			term_line = merged_index_reader.readline()
			
			if term_line == "":
				break

			term_info = term_line.split(";")
			term = term_info.pop(0)
			
			term_freq = log10(self._corpus.number_of_read_docs / len(term_info))
			new_term_info = ""

			for doc in term_info:
				gen_doc_info, term_weight = doc.split(":")
				doc_id, doc_len = gen_doc_info.split(",")
				real_weight = term_freq*(self._k1 + 1) * float(term_weight) / \
					(self._k1 * ((1 - self._b) + self._b * int(doc_len) / self._avg_doc_len) + float(term_weight))
				new_term_info += f";{doc_id}:{real_weight:.2f}"

			final_index_writer.write(f"{term}:{term_freq:.3f}" + new_term_info + "\n")

		merged_index_reader.close()
		os.remove(onlyfiles)
		final_index_writer.close()

		#avg_doc_len /= self._corpus.number_of_read_docs

		#for token in self._index:
		#	for info in self._index[token]:
		#		info.weight = self.get_token_freq(token) * (self._k1 + 1) * info.weight / \
		#		(self._k1 * ((1 - self._b) + self._b * doc_lens[info.doc] / avg_doc_len) + info.weight)
