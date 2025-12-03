import json
import os


path = "settings"
module_dir = os.path.dirname(os.path.abspath(__file__))
abs_path = os.path.join(module_dir, path)

_settings = "_settings.json"

silence_cutter = "silence_cutter" + _settings
silence_cutter_interval = "interval"
silence_cutter_threshold = "threshold"
silence_cutter_silence_enter_span = "silence_enter_span"
silence_cutter_silence_exit_span = "silence_exit_span"

def load_settings(filename):
    filepath = os.path.join(abs_path, filename)

    with open(filepath, 'r') as file:
        settings = json.load(file)

    return settings
