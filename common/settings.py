import json
import os


path = "settings"
module_dir = os.path.dirname(os.path.abspath(__file__))
abs_path = os.path.join(module_dir, path)

_settings = "_settings.json"

silence_cutter = "silence_cutter" + _settings
silence_cutter_interval = "interval"
silence_cutter_threshold = "threshold"

def load_settings(filename):
    filepath = os.path.join(abs_path, filename)

    with open(filepath, 'r') as file:
        settings = json.load(file)

    return settings
