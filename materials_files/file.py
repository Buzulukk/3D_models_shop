import uuid


class File:
    file_id: uuid.UUID

    def __init__(self, file_id: uuid.UUID):
        self.file_id = file_id
