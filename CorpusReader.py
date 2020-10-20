from csv import reader
import logging

logging.basicConfig(
	level=logging.INFO, format="%(message)s"
)

logger = logging.getLogger("CorpusReader")


class CorpusReader:
	def __init__(self, path):
		self.path = path
		self.proc_dict = {}

	def process(self):
		with open(self.path, "r") as filereader:
			filereader.readline()
			counter_id = 0
			for line in reader(filereader):
				if line[2] == "" or line[7] == "":
					continue

				self.proc_dict[counter_id] = (line[2], line[7])
				counter_id += 1
		return self.proc_dict
