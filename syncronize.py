import argparse


parser = argparse.ArgumentParser(
                    prog='Syncronize folders',
                    description='This script syncronizes two folders'
)

parser.add_argument('-s', '--source', required=True, help='Source folder path')
parser.add_argument('-r', '--replica', required=True, help='Path to replica folder')
parser.add_argument('-l', '--log', required=True, help='Path to log file')

