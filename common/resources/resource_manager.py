from common.resources.ffmpeg_resource import FFMPEGResource

class ResourceManager:
	def __init__(self):
		self.resources = {}

	def get_resource(self, media_item):
		if media_item.GetMediaId() not in self.resources:
			resource = self._load_resource(media_item)
			self.resources[media_item.GetMediaId()] = resource
			return resource

		return self.resources[media_item.GetMediaId()]

	def _load_resource(self, media_item):
		resource = FFMPEGResource(media_item)

		return resource
