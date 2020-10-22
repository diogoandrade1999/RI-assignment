from csv import reader


class CorpusReader:
	def __init__(self, path):
		self._path = path

	def process(self):
		proc_dict = {}
		with open(self._path, "r") as filereader:
			filereader.readline()
			for doc_id, line in enumerate(reader(filereader)):
				if line[2] != "" and line[7] != "":
					proc_dict[doc_id] = line[2] + " " + line[7]
		return proc_dict
