import os
from typing import Set

from folder_meta.meta_file import MetaFile


class MetaFolder:
    def __init__(self, path: str, expiration_time: int) -> None:
        """Class to represent a folder which can contain other 
        MetaFolder folders and MetaFile files.

        Args:
            path (str): folder directory 
            expiration_time (int): time for expiration
        """
        self.path = path
        self.meta = os.stat(path)
        self.expiration_time = expiration_time
        self.folders: Set[MetaFolder] = self._get_subfolders()
        self.files: Set[MetaFile] = self._get_files()

    @classmethod
    def _get_subfolders(cls) -> Set[MetaFolder]:
        directory_list: Set[MetaFolder] = Set([
            cls(path=dir, expiration_time=cls.expiration_time)
            for dir in os.listdir(cls.path)
            if os.path.isdir(dir)
        ])               

        return directory_list

    def _get_files(self) -> Set[MetaFile]:
        files_list: Set[MetaFile] = Set([
            MetaFile(path=dir, expiration_time=self.expiration_time)
            for dir in os.listdir(self.path)
            if os.path.isfile(dir)
        ])               

        return files_list
    
    def _eq_files(self, other: MetaFile) -> bool:
        for file, other_file in zip(self.files, other.files):
            if file != other_file:
                return False
        return True

    def __eq__(self, other: MetaFolder) -> bool:
        return self.path == other.path and \
            self.meta.st_size == other.meta.st_size and \
            (self.meta.st_mtime - other.meta.st_mtime) < self.expiration_time and \
            self.folders == other.folders and \
            self._eq_files()