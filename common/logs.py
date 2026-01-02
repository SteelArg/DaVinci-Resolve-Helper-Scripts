import datetime
from copy import copy

line_size = 20

def log_line(size=line_size):
	print("-"*size)

def log_thick_line(size=line_size):
	print("="*size)

def log_item(item, label="Item"):
	print(label)

	media_pool_item = item.GetMediaPoolItem()
	fps = "ERROR"
	if media_pool_item:
		fps = media_pool_item.GetClipProperty('FPS')

	print(f"Location | {item.GetStart()}, {item.GetEnd()}")
	print(f"Source   | {item.GetSourceStartFrame()}, {item.GetSourceEndFrame()}")
	print(f"FPS      | {fps}")


class LogTimer:
	def __init__(self, label="Timer"):
		self.label = label

		self.start_time = get_timestamp()
		self.timestamps = []
		self.running = True

	def timestamp(self):
		self.timestamps.append(get_timestamp())

	def stop(self):
		if not self.running:
			return

		running = False
		self.end_time = get_timestamp()

	def log_sections(self):
		self.stop()

		#all_timestamps = copy(self.timestamp)
		#all_timestamps.insert(0, self.start_time)
		#all_timestamps.append(self.end_time)
		
		print(self.label)

		prev_timestamp = self.start_time
		sections = copy(self.timestamps)
		sections.append(self.end_time)

		for timestamp in sections:
			duration = timestamp-prev_timestamp
			duration *= 1000.0
			print(f"(-) {str(duration)} ms")
			prev_timestamp = timestamp


def get_timestamp():
	return datetime.datetime.now().timestamp()
