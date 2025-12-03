import copy

from common.resolve_command import ResolveCommand
from common.item_adder import ItemAdder
import common.utils as utils
from common.logs import *


class GapsDeleter(ResolveCommand):
	def __init__(self, resolve):
		super().__init__(resolve)

		self.item_adder = ItemAdder(resolve)

	def delete_gaps(self, items):

		# Wrapper around __delete_gaps_internal() to handle linked items

		linked_item_indexes = []
		all_items = copy.copy(items)
		for item in items:
			item_index = all_items.index(item)
			
			item_handled = False
			for index_group in linked_item_indexes:
				if item_index in index_group:
					item_handled
			if item_handled:
				continue

			linked_index_group = [item_index]
			for linked_item in item.GetLinkedItems():
				if linked_item not in all_items:
					all_items.append(linked_item)
				linked_index_group.append(all_items.index(linked_item))
			
			if (linked_index_group.__len__() > 1):
				linked_item_indexes.append(linked_index_group)

		print(linked_item_indexes)

		for linked_index_group in linked_item_indexes:
			self._set_item_indexes_linked(linked_index_group, all_items, False)

		moved_items = self.__delete_gaps_internal(all_items)

		for linked_index_group in linked_item_indexes:
			self._set_item_indexes_linked(linked_index_group, moved_items, True)

		return moved_items


	def __delete_gaps_internal(self, items):
		# Calculate item locations
		item_locations = []
		i = 0
		for item in items:
			i += 1
			print("Item " + str(i))

			location = [item.GetStart(True), item.GetEnd(True)]
			intersected = False
			for other_location in copy.copy(item_locations):
				if (self._are_locations_intersecting(location, other_location)):
					intersected = True
					common_location = [min(location[0], other_location[0]), max(location[1], other_location[1])]
					item_locations.remove(other_location)
					item_locations.append(common_location)
					break
			if not intersected:
				item_locations.append(location)

		item_locations = sorted(item_locations, key=lambda location: location[0])

		print("locations: " + str(item_locations))

		# No gaps
		if (item_locations.__len__() < 2):
			print("no gaps")
			return items

		# Calculate gaps
		gaps = []
		for i in range(0, item_locations.__len__()-1):
			prev_location = item_locations[i]
			next_location = item_locations[i+1]

			gap = [prev_location[1], next_location[0]]
			gap.append(gap[1]-gap[0])
			
			gaps.append(gap)

		print("gaps: " + str(gaps))

		# Move each item
		moved_items = []

		i = 0
		for item in items:
			i += 1
			# Calculate gap distance
			gap_distance = 0.0
			for gap in gaps:
				if gap[0] > item.GetStart(True):
					break

				gap_distance += gap[2]

			resource = item.GetMediaPoolItem()
			source_location = [item.GetSourceStartFrame(), item.GetSourceEndFrame()]
			start_position = item.GetStart(True)
			(track_type, track) = item.GetTrackTypeAndIndex()
			media_type = utils.track_type_to_media_type(track_type)

			log_thick_line()

			log_item(item, f"#{i} Original")

			self.timeline.DeleteClips([item])

			moved_item = self.item_adder.add_item(
					resource, source_location[0], source_location[1],
					track, start_position - gap_distance, media_type
				)

			log_line()

			log_item(moved_item, f"#{i} Moved")

			moved_items.append(moved_item)

		return moved_items

	def _set_item_indexes_linked(self, index_group, items, value):
		linked_items = []
		for index in index_group:
			linked_items.append(items[index])
		
		self.timeline.SetClipsLinked(linked_items, value)


	def _are_locations_intersecting(self, a, b):
		if (a[0] > b[1]):
			return False

		if (a[1] < b[0]):
			return False

		return True
