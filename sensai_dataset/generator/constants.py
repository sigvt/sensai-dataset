import os

DATASET_DIR = os.environ['DATASET_DIR']
DATASET_SOURCE_DIR = os.environ['DATASET_SOURCE_DIR']

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(DATASET_SOURCE_DIR, exist_ok=True)
