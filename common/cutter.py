import math

from common.resolve_command import ResolveCommand
from common.item_adder import ItemAdder
import common.utils as utils


class Cutter(ResolveCommand):
	def __init__(self, resolve):
		super().__init__(resolve)
		self.media_pool = self.project.GetMediaPool()
		self.timeline = self.project.GetCurrentTimeline()

		self.item_adder = ItemAdder(resolve)

	# Pass an TimelineItem and an int frame position
	# Returns a list of two splitted items or a list of two lists if items were linked

	def cut(self, item, split_position):
		
		# Wrapper around __cut_internal() to handle linked items

		linked_items = item.GetLinkedItems()
		linked_items.append(item)

		# No linked items

		if linked_items.__len__() <= 1:
			return self.__cut_internal(item, split_position)

		# Handle linked items

		self.timeline.SetClipsLinked(linked_items, False)
		left_items = []
		right_items = []

		for item in linked_items:
			result = self.__cut_internal(item, split_position)
			left_items.append(result[0])
			right_items.append(result[1])

		self.timeline.SetClipsLinked(left_items, True)
		self.timeline.SetClipsLinked(right_items, True)

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
