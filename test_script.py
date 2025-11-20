from common.cutter import Cutter
from common.gaps_deleter import GapsDeleter

resolve = app.GetResolve()
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
timeline = project.GetCurrentTimeline()

cutter = Cutter(resolve)
gaps_deleter = GapsDeleter(resolve)

items = timeline.GetItemListInTrack("video", 1)

gaps_deleter.delete_gaps(items)
