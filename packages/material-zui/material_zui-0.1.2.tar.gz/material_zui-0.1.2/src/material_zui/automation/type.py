from typing import Optional

Video = dict[{'title': str,
              'description': str,
              'path': str,
              'playlist': Optional[str],
              'tags': Optional[list[str]],
              'is_publish': Optional[bool],
              'schedule': Optional[str]}]

Videos = list[Video]
