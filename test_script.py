import sys

from common.cutter import Cutter
from common.gaps_deleter import GapsDeleter
from common.resources.resource_manager import ResourceManager
from common.silence_cutter import SilenceCutter

resolve = app.GetResolve()
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
timeline = project.GetCurrentTimeline()

cutter = Cutter(resolve)
gaps_deleter = GapsDeleter(resolve)

items = timeline.GetItemListInTrack("audio", 1)

item = items[0]

media = item.GetMediaPoolItem()

resource_manager = ResourceManager()

resource = resource_manager.get_resource(media)

silence_cutter = SilenceCutter(resolve, resource_manager)

silence_cutter.cut_silence(item)

#print(resource.get_volume(3.0))
