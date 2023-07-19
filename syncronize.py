import argparse

from meta.meta_folder import MetaFolder
from sycnronizer.syncronizer import Syncronizer


EXPIRATION_TIME = 120


parser = argparse.ArgumentParser(
    prog='Syncronize folders',
    description='This script syncronizes two folders'
)

parser.add_argument('-s', '--source', required=True, help='Source folder path')
parser.add_argument('-r', '--replica', required=True, help='Path to replica folder')
parser.add_argument('-l', '--log', required=True, help='Path to log file')
args = parser.parse_args()

source_path: str = args.source
replica_path: str = args.replica
log_path: str = args.log

import logging
logging.basicConfig(
    filename=log_path, 
    encoding='utf-8', 
    level=logging.INFO, 
    format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S'
)
logging.info("Running Urban Planning")

logger = logging.getLogger('urbanGUI')
sync = Syncronizer(source_path=source_path, target_path=replica_path, logger=logger)

sync.syncronize()