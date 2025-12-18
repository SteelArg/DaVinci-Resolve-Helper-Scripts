import math

from common.resolve_command import ResolveCommand
from common.item_adder import ItemAdder, BatchItemAdder
import common.utils as utils


class BatchCutter(ResolveCommand):
	def __init__(self, resolve):
		super().__init__(resolve)

		self.item_adder = ItemAdder(resolve)
		self.batch_item_adder = BatchItemAdder(resolve)

	# Pass an TimelineItem and an int frame position
	# Returns two lists of splitted items that were linked

	# Wrapper around __cut_internal() to handle linked items

	def cut_batch(self, item, split_positions):
		return self.cut_batch_group([item], split_positions)

	def cut_batch_group(self, items, split_positions):
		linked_items = utils.LinkedItems(items, self.timeline)
		items = linked_items.all_items

		# Handle linked items

		linked_items.set_all_items_linked(False)
		cutted_items_rotated = []

		for item in items:
			self.__cut_batch_internal(item, split_positions)
			self.timeline.DeleteClips([item])
			result = self.batch_item_adder.execute()
			cutted_items_rotated.append(result)

		cutted_items_zipped = list(zip(*cutted_items_rotated))

		for cutted_items in cutted_items_zipped:
			linked_items.set_items(cutted_items)
			linked_items.set_all_items_linked(True)

		return cutted_items_zipped

	def __cut_batch_internal(self, item, split_positions):
		resource = item.GetMediaPoolItem()

		# Compute positions and data

		start_position = int(item.GetStart(False))

		source_start = item.GetSourceStartFrame()
		source_end = item.GetSourceEndFrame()

		frame_rate_conversion = float(self.timeline.GetMediaPoolItem().GetClipProperty("FPS")) / float(resource.GetClipProperty("FPS"))
		source_splits = []
		for split_position in split_positions:
			source_split = math.ceil((split_position - start_position) / frame_rate_conversion) + source_start
			source_splits.append(source_split)
		source_splits.append(source_end)

		# Track data
		(track_type, track) = item.GetTrackTypeAndIndex()
		media_type = utils.track_type_to_media_type(track_type)

		# Add items to the item adder

		split_positions.insert(0, start_position)
		prev_source_split = source_start

		for i in range(source_splits.__len__()):
			source_split = source_splits[i]
			split_position = split_positions[i]

			if source_split == prev_source_split:
				continue

			self.batch_item_adder.add_item(resource, prev_source_split, source_split, track, split_position, media_type)

			prev_source_split = source_split
