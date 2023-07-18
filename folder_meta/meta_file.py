import os


class MetaFile:
    def __init__(self, path: str, expiration_time: int) -> None:
        """Class to represent a file in terms of it state.

        Args:
            path (str): file directory 
            expiration_time (int): time for expiration
        """
        self.path = path
        self.meta = os.stat(path)
        self.expiration_time = expiration_time
        
    def __eq__(self, other: MetaFile) -> bool:
        return self.path == other.path and \
            self.meta.st_size == other.meta.st_size and \
            (self.meta.st_mtime - other.meta.st_mtime) < self.expiration_time