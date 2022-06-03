import argparse

from sensai_dataset.generator.commands import generate_dataset, generate_reduced_dataset
from sensai_dataset.generator.constants import SENSAI_COMPLETE_DIR, SENSAI_DIR, DATASET_SOURCE_DIR

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dataset generator')
    parser.add_argument('-m', '--matcher', type=str, default='chats_*.parquet')
    args = parser.parse_args()

    print('source: ' + DATASET_SOURCE_DIR)
    print('SENSAI_COMPLETE_DIR: ' + SENSAI_COMPLETE_DIR)
    print('SENSAI_DIR: ' + SENSAI_DIR)

    generate_dataset(source_dir=DATASET_SOURCE_DIR,
                     target_dir=SENSAI_COMPLETE_DIR,
                     matcher=args.matcher)

    generate_reduced_dataset(source_dir=DATASET_SOURCE_DIR,
                             target_dir=SENSAI_DIR,
                             matcher=args.matcher)
