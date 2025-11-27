import ffmpeg
import re

from common.resources.audio_resource import AudioResource


class FFMPEGResource(AudioResource):
	def __init__(self, media_item):
		self.file_path = media_item.GetClipProperty("File Path")
		self.frame_rate = media_item.GetClipProperty("FPS")
		self.frame_duration = 1.0 / self.frame_rate


	def get_volume(self, time_position):
		try:
			print("fasd")
			print(self.file_path)
			process = ffmpeg.input(self.file_path, ss=time_position, t=self.frame_duration).audio.filter(
				'astats', metadata=1
			).filter(
				'ametadata', mode='print', key='lavfi.astats.Overall.RMS_level'
			).output(
				'pipe:', format='null'
			).run(capture_stdout=True, capture_stderr=True)

			stderr_output = process[1].decode('utf-8')

			# Extract the RMS level from the stderr output
			match = re.search(r'lavfi\.astats\.Overall\.RMS_level=(-?\d+\.\d+)', stderr_output)
			if match:
				rms_level = float(match.group(1))
				return rms_level
			else:
				print(f"Could not find RMS level in FFmpeg output for time {target_time}s.")
				return None

		except ffmpeg.Error as e:
			print(f"FFmpeg error: {e.stderr.decode('utf-8')}")
			return None

		except Exception as e:
			print(f"An error occurred: {e}")
			return None
