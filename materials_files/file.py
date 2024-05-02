import uuid
from typing import Any


class File:
    file_id: Any

    def __init__(self, file_id: Any):
        self.file_id = file_id
