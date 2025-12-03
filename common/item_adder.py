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

		return self.media_pool.AppendToTimeline([clip_info])[0]
