import gc
from glob import iglob
import argparse
import shutil
from os.path import basename, join, splitext

import numpy as np
import pandas as pd

from sensai_gen.constants import DATASET_DIR, DATASET_SOURCE_DIR


def load_channels(**kwargs):
    dtype_dict = {
        'channelId': 'category',
        'name': 'category',
        'englishName': 'category',
        'affiliation': 'category',
        'group': 'category',
        'subscriptionCount': 'int32',
        'videoCount': 'int32',
        'photo': 'category'
    }
    channels = pd.read_csv(join(DATASET_SOURCE_DIR, 'channels.csv'),
                           dtype=dtype_dict,
                           **kwargs)
    return channels


def generate_dataset(matcher):
    print('[generate_sensai_dataset]')

    delet_path = join(DATASET_SOURCE_DIR, 'deletion_events.csv')
    del_events = pd.read_csv(delet_path, usecols=['id', 'retracted'])
    del_events = del_events.query('retracted == 0').copy()
    del_events.drop(columns=['retracted'], inplace=True)
    del_events['deleted'] = True

    ban_path = join(DATASET_SOURCE_DIR, 'ban_events.csv')
    ban_events = pd.read_csv(ban_path, usecols=['authorChannelId', 'videoId'])
    ban_events['banned'] = True

    for f in sorted(iglob(join(DATASET_SOURCE_DIR, matcher))):
        period_string = splitext(basename(f))[0].split('_')[1]
        print('>>> Period:', period_string)

        columns_to_use = [
            'body',
            'authorChannelId',
            'channelId',
            'membership',
            'id',
            'videoId',
        ]
        columns_to_delete = [
            'id',
            'videoId',
            'deleted',
            'banned',
        ]

        # load chat
        print('>>> Loading chats')
        chat_path = join(DATASET_SOURCE_DIR, 'chats_' + period_string + '.csv')
        chat_dtype = {
            'authorChannelId': 'category',
            'membership': 'category',
            'videoId': 'category',
            'channelId': 'category'
        }
        chats = pd.read_csv(chat_path, dtype=chat_dtype, usecols=columns_to_use)

        # apply mods
        print('>>> Merging deletion')
        chats = pd.merge(chats, del_events, on='id', how='left')
        chats['deleted'].fillna(False, inplace=True)

        # apply mods
        print('>>> Merging bans')
        chats = pd.merge(chats,
                         ban_events,
                         on=['authorChannelId', 'videoId'],
                         how='left')
        chats['banned'].fillna(False, inplace=True)

        flagged = chats[(chats['deleted'] | chats['banned'])].copy()

        # to make balanced dataset
        nbFlagged = flagged.shape[0]
        if nbFlagged == 0:
            continue

        print('>>> Sampling nonflagged chats')
        print('nbFlagged', nbFlagged)
        nonflag = chats[~(chats['deleted'] | chats['banned'])].sample(nbFlagged)

        print('>>> Writing dataset')

        flagged.drop(columns=columns_to_delete, inplace=True)
        flagged.to_csv(join(DATASET_DIR, f'chats_flagged_{period_string}.csv'),
                       index=False)
        nonflag.drop(columns=columns_to_delete, inplace=True)
        nonflag.to_csv(join(DATASET_DIR, f'chats_nonflag_{period_string}.csv'),
                       index=False)

        # free up memory
        del nonflag
        del flagged
        del chats
        gc.collect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dataset generator')
    parser.add_argument('-m', '--matcher', type=str, default='chats_*.csv')
    args = parser.parse_args()

    print('target: ' + DATASET_DIR)
    print('source: ' + DATASET_SOURCE_DIR)

    shutil.copy(join(DATASET_SOURCE_DIR, 'channels.csv'), DATASET_DIR)

    generate_dataset(matcher=args.matcher)
