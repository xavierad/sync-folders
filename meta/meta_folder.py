import logging
import os
from typing import List

from meta.meta_item import MetaFile


class MetaFolder:
    def __init__(self, path: str, logger: logging.Logger) -> None:
        """Class to represent a folder which can contain other 
        MetaFolder folders and MetaFile files.

        Args:
            path (str): folder directory 
        """
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self._meta = os.stat(path)
        self.folders: List[MetaFolder] = self._get_subfolders()
        self.files: List[MetaFile] = self._get_files()
        self.logger = logger

    
    def _get_subfolders(self) -> List:
        """Get folders under the folder directory.

        Returns:
            List[MetaFolder]: a list of MetaFolder folders
        """
        directory_list: List[MetaFolder] = [
            MetaFolder(path=dir)
            for dir in os.listdir(self.path)
            if os.path.isdir(dir)
        ]

        return directory_list

    def _get_files(self) -> List[MetaFile]:
        """Get files under the folder directory.

        Returns:
            List[MetaFile]: a list of MetaFile files
        """
        files_list: List[MetaFile] = [
            MetaFile(path=dir)
            for dir in os.listdir(self.path)
            if os.path.isfile(dir)
        ]

        return files_list
    
    def _get_files_to_sync(self, other: object) -> List[MetaFile]:
        """Checks if the files in this folder are equal to the 
        ones under the directory corresponding to other

        Args:
            other (MetaFolder): other folder

        Returns:
            bool: True if are the same
        """
        files_to_be_synced: List[MetaFile] = [
            file
            for file, other_file in zip(self.files, other.files)
            if file != other_file
        ]
                
        return files_to_be_synced

    def __eq__(self, other: object) -> List[MetaFile]:
        return self.path == other.path and \
            self._meta.st_size == other._meta.st_size and \
            self.folders == other.folders and \
            self._eq_files()
    
    def get_meta_stat(self) -> os.stat_result:
        return self._meta