# You can skip the generation of Model/Controller/Converter and Tests by supplying --bare to createcog
from discord import ActivityType


class ActivityTypeConverter:

    def __init__(self, value):
        self.cleaned_value = ActivityType.unknown
        if value == "listening":
            self.cleaned_value = ActivityType.listening
        elif value == 'playing':
            self.cleaned_value = ActivityType.playing
        elif value == 'streaming':
            self.cleaned_value = ActivityType.streaming
        elif value == 'watching':
            self.cleaned_value = ActivityType.watching
