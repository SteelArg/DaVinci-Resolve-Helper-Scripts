
class ResolveCommand:
	def __init__(self, resolve):
		self._resolve = resolve
		self._project_manager = self._resolve.GetProjectManager()
		self.project = self._project_manager.GetCurrentProject()
