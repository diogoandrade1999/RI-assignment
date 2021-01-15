import sys

from csv import reader
from os import path
from itertools import islice


class CorpusReader:
	"""
	Class used by process data files.

	...

	Attributes
	----------
	number_of_read_docs : int
		The number of read docs.

	Methods
	-------
	process()
		Process the data file.
		Return a dict with the data.
	"""
	def __init__(self, data_file_path:str):
		"""
		Parameters
		----------
		data_file_path : str
			The data file path.
		"""
		self._data_file_path = data_file_path
		self._doc_index = 0
		self._number_of_read_docs = 0

	@property
	def number_of_read_docs(self) -> int:
		return self._number_of_read_docs

	def process(self, number_of_files_to_read:int) -> tuple:
		"""
		Process the data file.

		Parameters
		----------
		number_of_files_to_read : int
			The number of files to read.

		Returns
		-------
		tuple
			A dict with the data as well as a boolean value checking if we have reached the end of file.
		"""
		if not path.exists(self._data_file_path) or not path.isfile(self._data_file_path):
			sys.exit("Data file not found!")

		proc_dict = {}
		read_docs = 0
		with open(self._data_file_path, "r") as filereader:
			for i in range(self._doc_index + 1):
				next(filereader)

			csv_reader = reader(filereader)
			for line in islice(csv_reader, number_of_files_to_read):
				if line[0] != "" and line[3] != "" and line[8] != "":
					proc_dict[line[0]] = line[3] + " " + line[8]
					self._number_of_read_docs += 1
				read_docs += 1

		self._doc_index += number_of_files_to_read
		return proc_dict, number_of_files_to_read != read_docs
