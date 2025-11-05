import re
from rest_framework.serializers import ValidationError


YOUTUBE_RE = re.compile(
    r'^https?://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}$'
)

class TitleLessonVideoUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not bool(YOUTUBE_RE.match(value)):
            raise ValidationError('Ссылка на видео должна вести на Ютуб')
