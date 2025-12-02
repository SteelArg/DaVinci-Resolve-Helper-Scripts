from common.logs import log_item
from common.resolve_command import ResolveCommand
from common.cutter import Cutter


interval = 2.0
threshold = -35.0

class SilenceCutter(ResolveCommand):
	def __init__(self, resolve, resource_manager):
		super().__init__(resolve)
		self.media_pool = self.project.GetMediaPool()
		self.cutter = Cutter(resolve)

		self.resource_manager = resource_manager

	def cut_silence(self, item):
		# Get volume data
		volume_data = []
		duration = item.GetDuration(False)
		print(duration)
		position = 0.0
		while position < duration:
			volume = self.get_item_volume(item, position)
			volume_data.append([position, volume])

			position += interval

		print(volume_data)

		# Get cut positions
		starts_with_silence = False
		prev_silence = True
		cuts = []
		for data in volume_data:
			silence = data[1] < threshold
			if silence is not prev_silence:
				cuts.append(data[0])

			if data[0] == 0.0:
				starts_with_silence = silence

			prev_silence = silence

		print(cuts)

		# Cut and delete
		offset = item.GetStart(False)
		new_item = item
		for cut in cuts:
			if cut == 0.0:
				continue

			cut_result = self.cutter.cut(new_item, cut + offset)
			print(cut_result)
			new_item = cut_result[1]
			log_item(new_item)

	def get_item_volume(self, item, local_frame_position):
		source_frame_position = local_frame_position + item.GetSourceStartFrame()
		media_item = item.GetMediaPoolItem()
		fps = float(media_item.GetClipProperty("FPS"))
		source_time_position = source_frame_position / fps

		resource = self.resource_manager.get_resource(media_item)
		return resource.get_volume(source_time_position)
