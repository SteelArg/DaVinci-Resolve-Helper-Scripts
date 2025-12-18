from common.resources.audio_resource import AudioResource
import common.utils as utils
from common.logs import log_item

class TimelineResource(AudioResource):
    def __init__(self, media_item, project, resource_manager):
        self.project = project
        self.media_item = media_item
        self.resource_manager = resource_manager

        self.frame_rate = float(media_item.GetClipProperty("FPS"))

        self.update_timeline_info()

    def get_volume(self, frame_position):
        frame_position += self.start_frame
        audio_clips = self._get_audio_clips_at_position(frame_position)
        total_linear_volume = 0
        print(frame_position)
        for audio_clip in audio_clips:
            #print("Audio Clip in Timeline : " + audio_clip)
            volume = self._get_audio_clip_volume(audio_clip, frame_position)
            linear_volume = utils.db_to_linear(volume)
            total_linear_volume += linear_volume
        total_volume = utils.linear_to_db(total_linear_volume)
        return total_volume

    def update_timeline_info(self):
        # Load the timeline
        timeline_count = self.project.GetTimelineCount()
        for i in range(timeline_count):
            index = i+1
            timeline = self.project.GetTimelineByIndex(index)
            if timeline.GetName() == self.media_item.GetClipProperty("Clip Name"):
                self.timeline = timeline

        prev_timeline = self.project.GetCurrentTimeline()
        self.project.SetCurrentTimeline(self.timeline)

        self.start_frame = int(utils.timeline_timecode_to_frame(self.timeline.GetStartTimecode(), self.frame_rate))
        print(f"Start frame : {self.start_frame}")

        # Get all items
        items = utils.get_all_item_from_timeline(self.timeline)
        audio_items = []
        for item in items:
            track_type, _ = item.GetTrackTypeAndIndex()
            if track_type == "audio":
                audio_items.append(item)
                log_item(item)

        self.audio_clips = []
        for audio_item in items:
            resource = self.resource_manager.get_resource(audio_item.GetMediaPoolItem())
            start = audio_item.GetStart(False)
            end = audio_item.GetEnd(False)
            source = audio_item.GetSourceStartFrame()
            audio_clip = [resource, start, end, source]
            self.audio_clips.append(audio_clip)

        self.project.SetCurrentTimeline(prev_timeline)

    def _get_audio_clips_at_position(self, frame_position):
        clips = []
        for audio_clip in self.audio_clips:
            if audio_clip[1] <= frame_position and audio_clip[2] > frame_position:
                clips.append(audio_clip)
        return clips

    def _get_audio_clip_volume(self, audio_clip, frame_position):
        local_frame_position = frame_position - audio_clip[1]
        source_position = local_frame_position + audio_clip[3]
        resource = audio_clip[0]
        return resource.get_volume(source_position)
