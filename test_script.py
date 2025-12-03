from common.cutter import Cutter
from common.gaps_deleter import GapsDeleter
from common.resources.resource_manager import ResourceManager
from common.silence_cutter import SilenceCutter

# Setup DaVinci Resolve
resolve = app.GetResolve()
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
timeline = project.GetCurrentTimeline()

# Setup DR Commands
cutter = Cutter(resolve)
gaps_deleter = GapsDeleter(resolve)
resource_manager = ResourceManager()
silence_cutter = SilenceCutter(resolve, resource_manager)

# Get an audio item
items = timeline.GetItemListInTrack("audio", 1)
item = items[0]
media_item = item.GetMediaPoolItem()

# Cut out silence
silence_cutter.cut_silence(item)
