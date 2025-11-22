from abc import ABC, abstractmethod


class AudioResource(ABC):
	@abstractmethod
	def get_volume(self, time_position):
		pass
