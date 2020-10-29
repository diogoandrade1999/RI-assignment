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
	data_file_path : str
		The data file path.

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
		self.__number_of_read_docs = 0

	def process(self, number_of_files_to_read) -> tuple:
		"""
		Process the data file.

		Returns
		-------
		dict
			A dict with the data.
		"""
		if not path.exists(self._data_file_path):
			sys.exit("Data file not found!")

		proc_dict = {}
		read_docs = 0
		with open(self._data_file_path, "r") as filereader:
			for i in range(1+self.__number_of_read_docs):
				next(filereader)

			csv_reader = reader(filereader)
			for doc_id, line in enumerate(islice(csv_reader, number_of_files_to_read)):
				if line[2] != "" and line[7] != "":
					proc_dict[doc_id] = line[2] + " " + line[7]
				read_docs += 1

		self.__number_of_read_docs += number_of_files_to_read
		return proc_dict, number_of_files_to_read != read_docs
