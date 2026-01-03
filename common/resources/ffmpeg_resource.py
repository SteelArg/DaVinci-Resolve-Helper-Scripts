import ffmpeg
import numpy as np
import math

from common.resources.audio_resource import AudioResource
import common.utils as utils


frame_size_samples = 1024

class FFMPEGResource(AudioResource):
	def __init__(self, media_item):
		self.file_path = media_item.GetClipProperty("File Path")
		self.frame_rate = float(media_item.GetClipProperty("FPS"))
		self.frame_duration = 1.0 / self.frame_rate

		self.load_volume_data()

	def load_volume_data(self):
		bytes_per_sample = 4
		sample_rate = 48000
		chunk_size_increment = float(sample_rate) / self.frame_rate
		chunk_size_int = math.floor(chunk_size_increment)
		chunk_leftover = chunk_size_increment - chunk_size_int

		process = (
			ffmpeg
			.input(self.file_path)
			.output(
				'pipe:',
				format='f32le',
				ac=1,
				ar=sample_rate
			)
			.run_async(pipe_stdout=True, pipe_stderr=False)
		)

		self.volumes = []

		leftover = 0.0

		while True:
			leftover += chunk_leftover
			current_chunk_size = chunk_size_int
			if leftover >= 1.0:
				leftover_int = math.floor(leftover)
				current_chunk_size += leftover_int
				leftover -= leftover_int

			buf = process.stdout.read(current_chunk_size * bytes_per_sample)
			if not buf:
				break

			samples = np.frombuffer(buf, dtype=np.float32)
			if samples.size == 0:
				break

			rms = np.sqrt(np.mean(samples**2))
			db = utils.linear_to_db(rms)

			self.volumes.append(db)

		self.max_frame = self.volumes.__len__() - 1

		process.wait()

	def get_volume(self, frame_position: float):
		frame_index = math.floor(frame_position)
		
		if (frame_index > self.max_frame):
			return utils.linear_to_db(0.0)
		
		volume = self.volumes[frame_index]

		return volume
