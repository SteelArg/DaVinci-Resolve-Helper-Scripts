import math

def track_type_to_media_type(track_type):
	match track_type:
		case "video":
			return 1
		case "audio":
			return 2
		case _:
			return 0
		
def get_all_item_from_timeline(timeline):
	all_items = []
	for track_type in ["video", "audio"]:
		track_count = timeline.GetTrackCount(track_type)
		for i in range(track_count):
			track_index = i+1
			items_in_track = timeline.GetItemListInTrack(track_type, track_index)
			for item in items_in_track:
				all_items.append(item)
	return all_items

def timeline_timecode_to_frame(timecode: str, fps: float) -> float:
	values = timecode.split(":")
	int_values = []
	for value in values:
		int_values.append(int(value))
	
	frames = int_values[3]
	seconds = int_values[2]
	minutes = int_values[1]
	hours = int_values[0]

	total_seconds = seconds + minutes * 60 + hours * 3600

	total_frame = frames + float(total_seconds) * fps

	return total_frame

def db_to_linear(db_value: float) -> float:
    return 10 ** (db_value / 20.0)

def linear_to_db(linear_value: float) -> float:
	if linear_value <= 1e-12:
		return -120.0
	return 20.0 * math.log10(linear_value)
