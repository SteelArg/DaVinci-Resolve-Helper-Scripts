from common.resources.ffmpeg_resource import FFMPEGResource
from common.resources.timeline_resource import TimelineResource

class ResourceManager:
	def __init__(self, project):
		self.project = project
		self.resources = {}

	def get_resource(self, media_item):
		if media_item.GetMediaId() not in self.resources:
			resource = self._load_resource(media_item)
			self.resources[media_item.GetMediaId()] = resource
			return resource

		return self.resources[media_item.GetMediaId()]

	def _load_resource(self, media_item):
		if media_item.GetClipProperty("Type") == "Timeline":
			return TimelineResource(media_item, self.project, self)
		else:
			return FFMPEGResource(media_item)
