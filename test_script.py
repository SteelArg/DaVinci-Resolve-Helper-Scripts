from common.cutter import Cutter
from common.gaps_deleter import GapsDeleter
from common.resources.resource_manager import ResourceManager
from common.silence_cutter import SilenceCutter

from common.logs import log_item

# Setup DaVinci Resolve
resolve = app.GetResolve()
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_pool = project.GetMediaPool()
timeline = project.GetCurrentTimeline()

# Setup DR Commands
resource_manager = ResourceManager()
silence_cutter = SilenceCutter(resolve, resource_manager)

# Get an audio item
items = timeline.GetItemListInTrack("audio", 1)
item = items[0]
media_item = item.GetMediaPoolItem()

# Cut out silence
silence_cutter.set_settings_from_item(item)
new_items = silence_cutter.cut_silence(item)
