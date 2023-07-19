import os
from typing import Set

from meta.meta_file import MetaFile


class MetaFolder:
    def __init__(self, path: str) -> None:
        """Class to represent a folder which can contain other 
        MetaFolder folders and MetaFile files.

        Args:
            path (str): folder directory 
        """
        self.path = path
        self._meta = os.stat(path)
        self.folders: Set[MetaFolder] = self._get_subfolders()
        self.files: Set[MetaFile] = self._get_files()

    @classmethod
    def _get_subfolders(cls) -> Set[MetaFolder]:
        """Get folders under the folder directory.

        Returns:
            Set[MetaFolder]: a set of MetaFolder folders
        """
        directory_list: Set[MetaFolder] = Set([
            cls(path=dir)
            for dir in os.listdir(cls.path)
            if os.path.isdir(dir)
        ])               

        return directory_list

    def _get_files(self) -> Set[MetaFile]:
        """Get files under the folder directory.

        Returns:
            Set[MetaFile]: a set of MetaFile files
        """
        files_list: Set[MetaFile] = Set([
            MetaFile(path=dir)
            for dir in os.listdir(self.path)
            if os.path.isfile(dir)
        ])               

        return files_list
    
    def _eq_files(self, other: MetaFolder) -> bool:
        """Checks if the files in this folder are equal to the 
        ones under the directory corresponding to other

        Args:
            other (MetaFolder): other folder

        Returns:
            bool: True if are the same
        """
        for file, other_file in zip(self.files, other.files):
            if file != other_file:
                return False
        return True

    def __eq__(self, other: MetaFolder) -> bool:
        return self.path == other.path and \
            self._meta.st_size == other._meta.st_size and \
            self.folders == other.folders and \
            self._eq_files()
    
    def get_meta_stat(self) -> os.stat_result:
        return self._meta