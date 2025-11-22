from common.resources.audio_resource import AudioResource


class FFMPEGResource(AudioResource):
	def __init__(self, file_path):
		self.file_path = file_path

	def get_volume(self, time_position):
		return 1.0
