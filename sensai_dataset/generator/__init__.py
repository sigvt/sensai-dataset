import argparse

from sensai_dataset.generator.commands import generate_dataset
from sensai_dataset.generator.constants import DATASET_DIR, DATASET_SOURCE_DIR

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dataset generator')
    parser.add_argument('-m', '--matcher', type=str, default='chats_*.csv')
    args = parser.parse_args()

    print('target: ' + DATASET_DIR)
    print('source: ' + DATASET_SOURCE_DIR)

    generate_dataset(source_dir=DATASET_SOURCE_DIR,
                     target_dir=DATASET_DIR,
                     matcher=args.matcher)
