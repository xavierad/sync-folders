import os


class MetaFile:
    def __init__(self, path: str) -> None:
        """Class to represent a file in terms of it state.

        Args:
            path (str): file directory 
        """
        self.path = path
        self._meta = os.stat(path)
        
    def __eq__(self, other: MetaFile) -> bool:
        return self.path == other.path and \
            self._meta.st_size == other._meta.st_size
    
    def get_meta_stat(self) -> os.stat_result:
        return self._meta