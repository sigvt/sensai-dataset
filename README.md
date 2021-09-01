# ❤️‍🩹 Sensai: Toxic Chat Dataset

Sensai is a dataset consists of live chats from all across Virtual YouTubers' live streams, ready for training toxic chat classification models.

Download the dataset from [Kaggle Datasets](https://www.kaggle.com/uetchy/sensai) and join `#livechat-dataset` channel on [holodata Discord](https://holodata.org/discord) for discussions.

## Provenance

- **Source:** YouTube Live Chat events (all streams covered by [Holodex](https://holodex.net), including Hololive, Nijisanji, 774inc, etc)
- **Temporal Coverage:** From 2021-01-15T05:15:33Z
- **Update Frequency:** At least once per month

## Research Ideas

- Toxic Chat Classification
- Spam Detection
- Sentence Transformer for Live Chats

See [public notebooks](https://www.kaggle.com/uetchy/sensai/code) for ideas.

## Files

| filename                  | summary                                                        | size     |
| ------------------------- | -------------------------------------------------------------- | -------- |
| `chats_flagged_%Y-%m.csv` | Chats flagged as either deleted or banned by mods (3,100,000+) | ~ 400 MB |
| `chats_nonflag_%Y-%m.csv` | Non-flagged chats (3,000,000+)                                 | ~ 300 MB |

To make it a balanced dataset, the number of `chats_nonflags` is adjusted (randomly sampled) to be the same as `chats_flagged`.
Ban and deletion are equivalent to `markChatItemsByAuthorAsDeletedAction` and `markChatItemAsDeletedAction` respectively.

## Dataset Breakdown

### Chats (`chats_%Y-%m.csv`)

| column          | type   | description                  |
| --------------- | ------ | ---------------------------- |
| timestamp       | string | UTC timestamp                |
| body            | string | chat message                 |
| membership      | string | membership status            |
| id              | string | anonymized chat id           |
| authorChannelId | string | anonymized author channel id |
| videoId         | string | source video id              |
| channelId       | string | source channel id            |

#### Membership status

| value             | duration                  |
| ----------------- | ------------------------- |
| unknown           | Indistinguishable         |
| non-member        | 0                         |
| less than 1 month | < 1 month                 |
| 1 month           | >= 1 month, < 2 months    |
| 2 months          | >= 2 months, < 6 months   |
| 6 months          | >= 6 months, < 12 months  |
| 1 year            | >= 12 months, < 24 months |
| 2 years           | >= 24 months              |

#### Pandas usage

Set `keep_default_na` to `False` and `na_values` to `''` in `read_csv`. Otherwise, chat message like `NA` would incorrectly be treated as NaN value.

```python
chats = pd.read_csv('../input/vtuber-livechat/chats_2021-03.csv',
                    na_values='',
                    keep_default_na=False,
                    index_col='timestamp',
                    parse_dates=True)
```

### Channels (`channels.csv`)

| column            | type            | description            |
| ----------------- | --------------- | ---------------------- |
| channelId         | string          | channel id             |
| name              | string          | channel name           |
| englishName       | nullable string | channel name (English) |
| affiliation       | string          | channel affiliation    |
| group             | nullable string | group                  |
| subscriptionCount | number          | subscription count     |
| videoCount        | number          | uploads count          |
| photo             | string          | channel icon           |

Inactive channels have `INACTIVE` in `group` column.

## Consideration

### Anonymization

`id` and `channelId` are anonymized by SHA-1 hashing algorithm with a pinch of undisclosed salt.

### Handling Custom Emojis

All custom emojis are replaced with a Unicode replacement character `U+FFFD`.

## Citation

```latex
@misc{sensai-dataset,
 author={Yasuaki Uechi},
 title={Sensai: Large Scale Virtual YouTubers Live Chat Dataset},
 year={2021},
 month={8},
 version={31},
 url={https://github.com/holodata/sensai-dataset}
}
```

## License

- Code: [MIT License](https://github.com/holodata/sensai-dataset/blob/master/LICENSE)
- Dataset: [ODC Public Domain Dedication and Licence (PDDL)](https://opendatacommons.org/licenses/pddl/1-0/index.html)
