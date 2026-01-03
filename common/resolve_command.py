
class ResolveCommand:
	def __init__(self, resolve):
		self._resolve = resolve
		self._project_manager = self._resolve.GetProjectManager()
		self.project = self._project_manager.GetCurrentProject()
		self.media_pool = self.project.GetMediaPool()
		self.timeline = self.project.GetCurrentTimeline()
		self.timeline_media_item = self.timeline.GetMediaPoolItem()

		self.frame_rate = float(self.timeline_media_item.GetClipProperty("FPS"))
