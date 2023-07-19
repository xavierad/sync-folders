import datetime
import logging
import os
import shutil
from meta.meta_folder import MetaFolder


class Syncronizer:
    def __init__(
            self, 
            source_path: str, 
            target_path: str, 
            logger: logging.Logger, 
            interval: int = 360,
            expiration_time: int = 360
) -> None:
        self.source = MetaFolder(path=source_path)
        self.target = MetaFolder(path=target_path)
        self.logger = logger
        self.interval = interval
        self.expiration_time = expiration_time
        
        self.logger.info('Syncronizer setup!')
        self.logger.info(f'Folder {self.source.path} will be syncronized to {self.target.path} every {self.interval} second(s)')    

    def _compare(self) -> bool:
        source_meta: os.stat_result = self.source.get_meta_stat()
        target_meta: os.stat_result = self.target.get_meta_stat()

        return self.source == self.target and \
            (source_meta.st_mtime - target_meta.st_mtime) <= self.expiration_time

    def syncronize(self) -> None:
        start_time = datetime.now()
        
        self.logger.info(f'Syncronizing started!')

        while True:
            if (datetime.now() - start_time).seconds == self.interval:
                try: 
                    if not os.path.exists(self.target.path):
                        os.makedirs(self.target.path)

                    self.logger.info('Syncronizing...')

                    if self._compare():
                        self.logger.info('')
                        shutil.move(self.source.path, self.target.path)
                except (KeyboardInterrupt, IOError, OSError, BaseException) as exception:
                    raise exception

            else:
                start_time = datetime.now()
            

            
