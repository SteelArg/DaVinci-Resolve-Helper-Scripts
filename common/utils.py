import copy
import math

def track_type_to_media_type(track_type):
	match track_type:
		case "video":
			return 1
		case "audio":
			return 2
		case _:
			return 0
		
class LinkedItems():
	def __init__(self, items, timeline):
		self.all_items = copy.copy(items)
		self.linked_item_index_groups = []

		self.timeline = timeline

		self._calculate_linked_items(items)

	def set_all_items_linked(self, value):
		for linked_item_index_group in self.linked_item_index_groups:
			self._set_item_index_group_linked(linked_item_index_group, value)

	def get_linked_items_by_index(self, index):
		return self.get_linked_items(self.get_item_by_index(index))

	def get_linked_items(self, item):
		linked_items = []
		linked_items.append(item)
		for linked_item_index_group in self.linked_item_index_groups:
			for linked_item_index in linked_item_index_group:
				linked_items.append(self.all_items[linked_item_index])
			
		return linked_items
	
	def set_items(self, new_items):
		self._calculate_all_items(new_items)
	
	def get_item_by_index(self, index):
		return self.all_items[index]
	
	def get_item_index(self, item):
		return self.all_items.index(item)
	
	def _set_item_index_group_linked(self, item_index_group, value):
		item_group = []
		for item_index in item_index_group:
			item_group.append(self.all_items[item_index])
		
		self.timeline.SetClipsLinked(item_group, value)

	def _calculate_linked_items(self, items):
		self.linked_item_index_groups = []

		for item in items:
			item_index = self.all_items.index(item)
			
			item_handled = False
			for index_group in self.linked_item_index_groups:
				if item_index in index_group:
					item_handled = True
			if item_handled:
				continue

			linked_index_group = [item_index]
			for linked_item in item.GetLinkedItems():
				if linked_item not in self.all_items:
					self.all_items.append(linked_item)
				linked_index_group.append(self.all_items.index(linked_item))
			
			if (linked_index_group.__len__() > 1):
				self.linked_item_index_groups.append(linked_index_group)

	def _calculate_all_items(self, items):
		self.all_items = copy.copy(items)
		for item in items:
			linked_items = item.GetLinkedItems()
			if linked_items is None:
				continue
			for linked_item in linked_items:
				if linked_item not in self.all_items:
					self.all_items.append(linked_item)

def get_all_item_from_timeline(timeline):
	all_items = []
	for track_type in ["video", "audio"]:
		track_count = timeline.GetTrackCount(track_type)
		for i in range(track_count):
			track_index = i+1
			items_in_track = timeline.GetItemListInTrack(track_type, track_index)
			for item in items_in_track:
				all_items.append(item)
	return all_items

def timeline_timecode_to_frame(timecode: str, fps: float) -> float:
	values = timecode.split(":")
	int_values = []
	for value in values:
		int_values.append(int(value))
	
	frames = int_values[3]
	seconds = int_values[2]
	minutes = int_values[1]
	hours = int_values[0]

	total_seconds = seconds + minutes * 60 + hours * 3600

	total_frame = frames + float(total_seconds) * fps

	return total_frame

def db_to_linear(db_value: float) -> float:
    return 10 ** (db_value / 20.0)

def linear_to_db(linear_value: float) -> float:
	if linear_value <= 1e-12:
		return -120.0
	return 20.0 * math.log10(linear_value)
