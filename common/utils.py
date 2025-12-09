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

def db_to_linear(db_value: float) -> float:
    return 10 ** (db_value / 20.0)

def linear_to_db(linear_value: float) -> float:
	if linear_value <= 1e-12:
		return -120.0
	return 20.0 * math.log10(linear_value)
