from csv import reader


class CorpusReader:
	def __init__(self, path):
		self._path = path

	def process(self):
		proc_dict = {}
		doc_id = 0
		with open(self._path, "r") as filereader:
			filereader.readline()
			for line in reader(filereader):
				if line[2] != "" and line[7] != "":
					proc_dict[doc_id] = line[2] + " " + line[7]
					doc_id += 1
		return proc_dict
