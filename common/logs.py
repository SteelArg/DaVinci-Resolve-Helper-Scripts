
line_size = 20

def log_line(size=line_size):
	print("-"*size)

def log_thick_line(size=line_size):
	print("="*size)

def log_item(item, label="Item"):
	print(label)
	print(f"Location | {item.GetStart()}, {item.GetEnd()}")
	print(f"Source   | {item.GetSourceStartFrame()}, {item.GetSourceEndFrame()}")
	print(f"FPS      | {item.GetMediaPoolItem().GetClipProperty('FPS')}")
