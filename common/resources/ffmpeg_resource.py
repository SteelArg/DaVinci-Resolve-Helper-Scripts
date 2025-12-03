import ffmpeg
import numpy as np

from common.resources.audio_resource import AudioResource


frame_size_samples = 1024

class FFMPEGResource(AudioResource):
	def __init__(self, media_item):
		self.file_path = media_item.GetClipProperty("File Path")
		self.frame_rate = float(media_item.GetClipProperty("FPS"))
		self.frame_duration = 1.0 / self.frame_rate

		self.load_volume_data()

	def load_volume_data(self):
		sample_rate = 48000
		chunk_size = int(sample_rate / self.frame_rate)

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

		bytes_per_sample = 4
		bytes_per_chunk = chunk_size * bytes_per_sample

		self.volumes = []

		while True:
			buf = process.stdout.read(bytes_per_chunk)
			if not buf:
				break

			samples = np.frombuffer(buf, dtype=np.float32)
			if samples.size == 0:
				break

			rms = np.sqrt(np.mean(samples**2))
			db = self.rms_to_db(rms)

			self.volumes.append(db)

		process.wait()
	
	def rms_to_db(self, rms):
		if rms <= 1e-12:
			return -120.0
		
		return 20.0 * np.log10(rms)

	def get_volume(self, frame_position):
		return self.volumes[frame_position]
