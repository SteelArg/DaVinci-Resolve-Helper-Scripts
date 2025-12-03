from common.logs import log_item, LogTimer
from common.resolve_command import ResolveCommand
from common.cutter import Cutter
import common.settings as settings


class SilenceCutter(ResolveCommand):
	def __init__(self, resolve, resource_manager):
		super().__init__(resolve)
		self.media_pool = self.project.GetMediaPool()
		self.cutter = Cutter(resolve)

		self.resource_manager = resource_manager

		self.set_settings(settings.load_settings(settings.silence_cutter))

	def set_settings(self, data):
		self.settings = data
		self.interval = data[settings.silence_cutter_interval]
		self.threshold = data[settings.silence_cutter_threshold]

	def cut_silence(self, item):
		total_log_timer = LogTimer("Cut Out Silence")
		volume_getter_timer = LogTimer("Get Volume")

		# Get volume data
		volume_data = []
		duration = item.GetDuration(False)
		position = 0
		while position < duration:
			volume = self.get_item_volume(item, position)
			volume_data.append([position, volume])

			volume_getter_timer.timestamp()

			position += self.interval

		volume_getter_timer.stop()
		total_log_timer.timestamp()

		# Get cut positions
		starts_with_silence = False
		prev_silence = True
		cuts = []
		for data in volume_data:
			silence = data[1] < self.threshold
			if silence is not prev_silence:
				cuts.append(data[0])

			if data[0] == 0.0:
				starts_with_silence = silence

			prev_silence = silence

		total_log_timer.timestamp()

		# Cut and delete
		offset = item.GetStart(False)
		new_item = item
		for cut in cuts:
			if cut == 0.0:
				continue

			cut_result = self.cutter.cut(new_item, cut + offset)
			new_item = cut_result[1]

		total_log_timer.stop()

		total_log_timer.log_sections()
		volume_getter_timer.log_sections()

	def get_item_volume(self, item, local_frame_position):
		source_frame_position = int(local_frame_position + item.GetSourceStartFrame())
		media_item = item.GetMediaPoolItem()
		resource = self.resource_manager.get_resource(media_item)

		return resource.get_volume(source_frame_position)
