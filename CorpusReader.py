import sys

from csv import reader


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

	def process(self) -> dict:
		"""
		Process the data file.

		Returns
		-------
		dict
			A dict with the data.
		"""
		try:
			proc_dict = {}
			with open(self._data_file_path, "r") as filereader:
				filereader.readline()
				for doc_id, line in enumerate(reader(filereader)):
					if line[2] != "" and line[7] != "":
						proc_dict[doc_id] = line[2] + " " + line[7]
			return proc_dict
		except FileNotFoundError as e:
			sys.exit("Data File not found!")
