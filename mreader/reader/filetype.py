import enum


class FileType(enum.Enum):
    song = 1
    image = 2

    def __str__(self):
        return self.name
