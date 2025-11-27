import sys

print(sys.executable)

from common.cutter import Cutter
from common.gaps_deleter import GapsDeleter
from common.resources.resource_manager import ResourceManager

resolve = app.GetResolve()
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
timeline = project.GetCurrentTimeline()

cutter = Cutter(resolve)
gaps_deleter = GapsDeleter(resolve)

items = timeline.GetItemListInTrack("audio", 1)

media = items[0].GetMediaPoolItem()

resource_manager = ResourceManager()

resource = resource_manager.get_resource(media)

print(resource.get_volume(3.0))
