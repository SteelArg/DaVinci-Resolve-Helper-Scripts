import math
import copy

from common.resolve_command import ResolveCommand
from common.item_adder import ItemAdder
import common.utils as utils


class Cutter(ResolveCommand):
	def __init__(self, resolve):
		super().__init__(resolve)

		self.item_adder = ItemAdder(resolve)

	# Pass an TimelineItem and an int frame position
	# Returns two lists of splitted items that were linked

	# Wrapper around __cut_internal() to handle linked items

	def cut_group(self, items, split_position):
		linked_items = utils.LinkedItems(items)
		items = linked_items.all_items

		# Handle linked items

		linked_items.set_all_items_linked(False)

		left_items = []
		right_items = []

		for item in items:
			result = self.__cut_internal(item, split_position)
			left_items.append(result[0])
			right_items.append(result[1])

		linked_items.set_items(left_items)
		linked_items.set_all_items_linked(True)
		linked_items.set_items(right_items)
		linked_items.set_all_items_linked(True)

		return [left_items, right_items]

	def __cut_internal(self, item, split_position):
		resource = item.GetMediaPoolItem()

		# Compute positions and data

		start_position = item.GetStart(True)
		end_position = item.GetEnd(True)
		split_position = int(split_position)

		split_percentage = (split_position-start_position) / (end_position-start_position)

		source_start = item.GetSourceStartFrame()
		source_end = item.GetSourceEndFrame()

		frame_rate_conversion = float(self.timeline.GetMediaPoolItem().GetClipProperty("FPS")) / float(resource.GetClipProperty("FPS"))
		source_split = math.ceil((split_position - start_position) / frame_rate_conversion) + source_start

		# Track data

		(track_type, track) = item.GetTrackTypeAndIndex()
		media_type = utils.track_type_to_media_type(track_type)

		# Delete clip
		self.timeline.DeleteClips([item])

		# Add first clip
		item1 = self.item_adder.add_item(resource, source_start, source_split, track, start_position, media_type)

		# Add second clip
		item2 = self.item_adder.add_item(resource, source_split, source_end, track, split_position, media_type)

		return [item1, item2]
