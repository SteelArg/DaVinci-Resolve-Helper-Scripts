from common.resolve_command import ResolveCommand


class ItemAdder(ResolveCommand):
	def __init__(self, resolve):
		super().__init__(resolve)

	def add_item(self, resource, source_start, source_end, track, record_frame, media_type=0):
		clip_info = {
			"mediaPoolItem" : resource,
			"startFrame" : source_start,
			"endFrame" : source_end,
			"trackIndex" : track,
			"recordFrame" : record_frame,
			"mediaType" : media_type
		}

		appended_clips = self.media_pool.AppendToTimeline([clip_info])

		return appended_clips[0]
	
class BatchItemAdder(ResolveCommand):
	def __init__(self, resolve):
		super().__init__(resolve)

		self.items_queue = []

	def add_item(self, resource, source_start, source_end, track, record_frame, media_type=0):
		clip_info = {
			"mediaPoolItem" : resource,
			"startFrame" : source_start,
			"endFrame" : source_end,
			"trackIndex" : track,
			"recordFrame" : record_frame,
			"mediaType" : media_type
		}

		self.items_queue.append(clip_info)

	def execute(self):
		result = self.media_pool.AppendToTimeline(self.items_queue)

		self.items_queue.clear()

		return result
