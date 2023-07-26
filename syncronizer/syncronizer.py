import logging
import os
import shutil
import time
from typing import List


class Syncronizer:
    def __init__(
            self, 
            source_path: str, 
            target_path: str, 
            logger: logging.Logger, 
            interval: int = 10,
            expiration_time: int = 360
) -> None:
        self.source_path = source_path
        self.target_path = target_path

        if not os.path.exists(target_path):
            os.makedirs(target_path)
        
        self.logger = logger
        self.interval = interval
        self.expiration_time = expiration_time
        
        self.logger.info('Syncronizer setup!')
        self.logger.info(f'Folder <{self.source_path}> will be syncronized to <{self.target_path}> every {self.interval} second(s)')    

    def _is_same(self, source: str, target: str) -> bool:
        return os.stat(source).st_size == os.stat(target).st_size
    
    def _copy_item(self, item: str, target: str) -> None:
        if os.path.isfile(item):
            shutil.copyfile(item, target)
            return
        shutil.copytree(item, target)

    def _copy_items(self, root: str, directories: List[str], items: List[str]) -> List[str]:
        for item in items:
            source_item = os.path.join(root, item)
            item_in_replica = source_item.replace(self.source_path, self.target_path)

            directories.append(item)
            if not os.path.exists(item_in_replica):
                self._copy_item(source_item, item_in_replica)
                self.logger.info(f'CREATED - Synced {source_item} -> {item_in_replica}')
            elif not self._is_same(source_item, item_in_replica):
                shutil.rmtree(item_in_replica)
                self._copy_item(source_item, item_in_replica)
                self.logger.info(f'COPY - Synced {source_item} -> {item_in_replica}')
            else:
                self.logger.info(f'No changes detected in {source_item}')
        return directories

    def _check_source(self, directories: List[str]) -> List[str]:
        for root, dirs, files in os.walk(self.source_path):
            directories = self._copy_items(root=root, directories=directories, items=dirs)
            directories = self._copy_items(root=root, directories=directories, items=files)

        return directories

    def _check_target(self, directories: List[str]) -> None:
        for _, dirs, files in os.walk(self.target_path):
            for file in files:
                replica_item: str = os.path.join(self.target_path, file)
                if file not in directories:
                    os.remove(replica_item)
                    self.logger.info(f'REMOVE - Removed {replica_item}')

            for dir in dirs:
                replica_item: str = os.path.join(self.target_path, dir)

                if dir not in directories:
                    shutil.rmtree(replica_item)
                    self.logger.info(f'REMOVE - Removed {replica_item}')

    def _sync(self) -> None:
        directories_to_sync: List[str] = self._check_source(directories=[])
        self._check_target(directories=directories_to_sync)

    def syncronize(self) -> None:
        
        self.logger.info(f'Syncronizing started!')
        self._sync()
        while True:
            time.sleep(self.interval)
            try: 
                self.logger.info('Checking for changes...')
                self._sync()

            except (KeyboardInterrupt, IOError, OSError, BaseException) as exception:
                self.logger.info(f'Syncronizing finished!')
                raise exception



            

            

            
