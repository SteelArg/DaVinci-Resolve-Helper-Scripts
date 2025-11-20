def track_type_to_media_type(track_type):
	match track_type:
		case "video":
			return 1
		case "audio":
			return 2
		case _:
			return 0
