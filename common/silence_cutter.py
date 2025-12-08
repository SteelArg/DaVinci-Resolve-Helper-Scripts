import copy

from common.logs import log_item, LogTimer
from common.resolve_command import ResolveCommand
from common.cutter import Cutter
import common.settings as settings


class SilenceCutter(ResolveCommand):
	def __init__(self, resolve, resource_manager):
		super().__init__(resolve)
		self.cutter = Cutter(resolve)

		self.resource_manager = resource_manager

		self.set_settings(settings.load_settings(settings.silence_cutter))

	def set_settings(self, data):
		self.settings = data
		self.interval = data[settings.silence_cutter_interval]
		self.threshold = data[settings.silence_cutter_threshold]
		self.silence_enter_span = data[settings.silence_cutter_silence_enter_span]
		self.silence_exit_span = data[settings.silence_cutter_silence_exit_span]

	def set_settings_from_item(self, item, duration=72, threshold_percentage=0.45):
		resource = self.resource_manager.get_resource(item.GetMediaPoolItem())
		source_start_frame = item.GetSourceStartFrame()
		max_volume = -120
		min_volume = 0
		
		for i in range(duration):
			volume = resource.get_volume(source_start_frame + i)
			max_volume = max(max_volume, volume)
			min_volume = min(min_volume, volume)

		self.threshold = max_volume*threshold_percentage + min_volume*(1-threshold_percentage)
		self.settings[settings.silence_cutter_threshold] = self.threshold

		print(f"Cut Out Silence Threshold: {self.threshold} db")

	def cut_silence(self, item):
		total_log_timer = LogTimer("Cut Out Silence")

		# Get volume data
		volume_data = []
		duration = item.GetDuration(False)
		position = 0
		while position < duration:
			volume = self.get_item_volume(item, position)
			volume_data.append([position, volume])

			position += self.interval
		
		total_log_timer.timestamp()

		# Get cut positions
		prev_cut_silence = True
		last_consideration = 0
		considering_cut = False
		cuts = []
		for data in volume_data:
			silence = data[1] < self.threshold
			if (not considering_cut) and silence is not prev_cut_silence:
				considering_cut = True
				last_consideration = data[0]

			if considering_cut and silence is prev_cut_silence:
				considering_cut = False

			frames_since_last_consideration = data[0] - last_consideration
			cut_span = self.silence_enter_span if silence else self.silence_exit_span

			if considering_cut and frames_since_last_consideration >= cut_span:
				cuts.append(last_consideration)
				considering_cut = False
				prev_cut_silence = silence

		starts_with_silence = True
		if cuts.__len__() > 0 and cuts[0] == 0:
			starts_with_silence = False
		
		total_log_timer.timestamp()

		# Cut and delete
		offset = item.GetStart(False)
		cutted_items = []
		new_item = item
		for cut in cuts:
			if cut == 0.0:
				continue

			cut_result = self.cutter.cut(new_item, cut + offset)
			cutted_items.append(cut_result[0][0])
			new_item = cut_result[1][1]

		cutted_items.append(new_item)

		cut_current_item = starts_with_silence
		items_to_delete = []
		for cutted_item in copy.copy(cutted_items):
			if cut_current_item:
				items_to_delete.append(cutted_item)
				cutted_items.remove(cutted_item)
			
			cut_current_item = not cut_current_item

		self.timeline.DeleteClips(items_to_delete)

		total_log_timer.stop()

		total_log_timer.log_sections()

		return cutted_items

	def get_item_volume(self, item, local_frame_position):
		source_frame_position = int(local_frame_position + item.GetSourceStartFrame())
		media_item = item.GetMediaPoolItem()
		resource = self.resource_manager.get_resource(media_item)

		return resource.get_volume(source_frame_position)
	