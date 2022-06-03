import gc
from glob import iglob
from os.path import basename, join, splitext

import pandas as pd


def generate_dataset(source_dir, target_dir, matcher):
    print('[generate_dataset]')

    delet_path = join(source_dir, 'deletion_events.parquet')
    del_events = pd.read_parquet(delet_path, columns=['id', 'retracted'])
    del_events = del_events.query('retracted == 0').copy()
    del_events.drop(columns=['retracted'], inplace=True)
    del_events['label'] = 'deleted'

    ban_path = join(source_dir, 'ban_events.parquet')
    ban_events = pd.read_parquet(ban_path,
                                 columns=['authorChannelId', 'videoId'])
    ban_events['label'] = 'hidden'

    for f in sorted(iglob(join(source_dir, matcher))):
        period_string = splitext(basename(f))[0].split('_')[1]
        print('>>> Period:', period_string)

        # load chat
        print('>>> Loading chats')
        chat_path = join(source_dir, 'chats_' + period_string + '.parquet')

        chats = pd.read_parquet(
            chat_path,
            columns=['authorChannelId', 'videoId', 'id', 'authorName', 'body'])

        # remove NA
        chats = chats[chats['body'].notna()]

        # apply mods
        print('>>> Merging bans')
        chats = pd.merge(chats,
                         ban_events,
                         on=['authorChannelId', 'videoId'],
                         how='left')

        # apply mods
        print('>>> Merging deletion')
        chats.loc[chats['id'].isin(del_events['id']), 'label'] = 'deleted'

        # apply safe
        print('>>> Applying safe')
        chats['label'].fillna('nonflagged', inplace=True)

        isFlagged = chats['label'] != 'nonflagged'
        flagged = chats[isFlagged].copy()

        # to make balanced dataset
        nbFlagged = flagged.shape[0]
        if nbFlagged == 0:
            continue

        print('>>> Sampling nonflagged chats')
        print('nbFlagged', nbFlagged)
        nonflag = chats[~isFlagged].sample(nbFlagged)

        print('>>> Writing dataset')

        # NOTE: do not use categorical type with to_parquest. otherwise, it will be failed to load them with huggingface's Dataset
        columns_to_delete = [
            'authorChannelId',
            'videoId',
            'id',
        ]

        flagged.drop(columns=columns_to_delete, inplace=True)
        flagged.to_parquet(join(target_dir,
                                f'chats_flagged_{period_string}.parquet'),
                           index=False)

        nonflag.drop(columns=columns_to_delete, inplace=True)
        nonflag.to_parquet(join(target_dir,
                                f'chats_nonflag_{period_string}.parquet'),
                           index=False)

        # free up memory
        del nonflag
        del flagged
        del chats
        gc.collect()


def generate_reduced_dataset(source_dir, target_dir, matcher):
    print('[generate_reduced_dataset]')

    delet_path = join(source_dir, 'deletion_events.parquet')
    del_events = pd.read_parquet(delet_path, columns=['id', 'retracted'])
    del_events = del_events.query('retracted == 0').copy()
    del_events.drop(columns=['retracted'], inplace=True)
    del_events['label'] = 'deleted'

    ban_path = join(source_dir, 'ban_events.parquet')
    ban_events = pd.read_parquet(ban_path,
                                 columns=['authorChannelId', 'videoId'])
    ban_events['label'] = 'hidden'

    for f in sorted(iglob(join(source_dir, matcher))):
        period_string = splitext(basename(f))[0].split('_')[1]
        print('>>> Period:', period_string)

        # load chat
        print('>>> Loading chats')
        chat_path = join(source_dir, 'chats_' + period_string + '.parquet')

        chats = pd.read_parquet(
            chat_path,
            columns=['authorChannelId', 'videoId', 'id', 'authorName', 'body'])

        # remove NA
        chats = chats[chats['body'].notna()]

        # apply mods
        print('>>> Merging bans')
        chats = pd.merge(chats,
                         ban_events,
                         on=['authorChannelId', 'videoId'],
                         how='left')

        # apply mods
        print('>>> Merging deletion')
        chats.loc[chats['id'].isin(del_events['id']), 'label'] = 'deleted'

        # apply safe
        print('>>> Applying safe')
        chats['label'].fillna('nonflagged', inplace=True)

        isFlagged = chats['label'] != 'nonflagged'
        flagged = chats[isFlagged].copy()

        # to make balanced dataset
        nbFlagged = flagged.shape[0]
        if nbFlagged == 0:
            continue

        print('>>> Sampling nonflagged chats')
        print('nbFlagged', nbFlagged)
        nonflag = chats[~isFlagged].sample(nbFlagged)

        print('>>> Writing dataset')

        # NOTE: do not use categorical type with to_parquest. otherwise, it will be failed to load them with huggingface's Dataset
        columns_to_delete = [
            'authorChannelId',
            'videoId',
            'id',
        ]

        flagged.drop(columns=columns_to_delete, inplace=True)
        flagged.to_parquet(join(target_dir,
                                f'chats_flagged_{period_string}.parquet'),
                           index=False)

        nonflag.drop(columns=columns_to_delete, inplace=True)
        nonflag.to_parquet(join(target_dir,
                                f'chats_nonflag_{period_string}.parquet'),
                           index=False)

        # free up memory
        del nonflag
        del flagged
        del chats
        gc.collect()
