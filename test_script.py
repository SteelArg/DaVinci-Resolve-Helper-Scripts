from common.cutter import Cutter
from common.gaps_deleter import GapsDeleter
from common.resources.resource_manager import ResourceManager
from common.silence_cutter import SilenceCutter
from common.logs import log_item

# Setup DaVinci Resolve
resolve = app.GetResolve()
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
timeline = project.GetCurrentTimeline()

# Setup DR Commands
cutter = Cutter(resolve)
gaps_deleter = GapsDeleter(resolve)
resource_manager = ResourceManager(project)
silence_cutter = SilenceCutter(resolve, resource_manager)

# Get an audio item
items = timeline.GetItemListInTrack("audio", 1)
item = items[0]
media_item = item.GetMediaPoolItem()
resource = resource_manager.get_resource(media_item)

log_item(item, "Timeline Item")
print(resource.get_volume(11))
print(resource.get_volume(758))

# Cut out silence
silence_cutter.set_settings_from_item(item)
silence_cutter.cut_silence(item)
