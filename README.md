# ❤️‍🩹 Sensai: Toxic Chat Dataset

Sensai is a toxic chat dataset consists of live chats from Virtual YouTubers' live streams.

Download the dataset from [Huggingface Hub](https://huggingface.co/datasets/holodata/sensai) or alternatively from [Kaggle Datasets](https://www.kaggle.com/uetchy/sensai).

Join `#livechat-dataset` channel on [holodata Discord](https://holodata.org/discord) for discussions.

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
| `chats_nonflag_%Y-%m.csv` | Non-flagged chats (3,100,000+)                                 | ~ 300 MB |

To make it a balanced dataset, the number of `chats_nonflags` is adjusted (randomly sampled) to be the same as `chats_flagged`.
Ban and deletion are equivalent to `markChatItemsByAuthorAsDeletedAction` and `markChatItemAsDeletedAction` respectively.

## Dataset Breakdown

### Chats (`chats_%Y-%m.parquet`)

| column          | type   | description                   |
| --------------- | ------ | ----------------------------- |
| body            | string | chat message                  |
| authorChannelId | string | anonymized author channel id  |
| channelId       | string | source channel id             |
| label           | string | {deleted, hidden, nonflagged} |

## Usage

### Pandas

```python
import pandas as pd
from glob import glob

df = pd.concat([pd.read_parquet(x) for x in glob('../input/sensai/*.parquet')], ignore_index=True)
```

### Huggingface Transformers

https://huggingface.co/docs/datasets/loading_datasets.html

```python
# $ pip3 install datasets
from datasets import load_dataset, Features, ClassLabel, Value

dataset = load_dataset("holodata/sensai",
    features=Features(
        {
            "body": Value("string"),
            "toxic": ClassLabel(num_classes=2, names=['0', '1'])
        }
    ))

model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=2)
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

def tokenize_function(examples):
    return tokenizer(examples["body"], padding="max_length", truncation=True)

tokenized_datasets = dataset['train'].shuffle().select(range(50000)).map(tokenize_function, batched=True)
tokenized_datasets.rename_column_("toxic", "label")
splitset = tokenized_datasets.train_test_split(0.2)
training_args = TrainingArguments("test_trainer")

trainer = Trainer(
    model=model, args=training_args, train_dataset=splitset['train'], eval_dataset=splitset['test']
)

trainer.train()
```

### Tangram

```bash
python3 ./examples/prepare_tangram_dataset.py
tangram train --file ./tangram_input.csv --target label
```

## Consideration

### Anonymization

`authorChannelId` are anonymized by SHA-1 hashing algorithm with a pinch of undisclosed salt.

### Handling Custom Emojis

All custom emojis are replaced with a Unicode replacement character `U+FFFD`.

## Citation

```latex
@misc{sensai-dataset,
 author={Yasuaki Uechi},
 title={Sensai: Toxic Chat Dataset},
 year={2021},
 month={8},
 version={31},
 url={https://github.com/holodata/sensai-dataset}
}
```

## License

- Code: [MIT License](https://github.com/holodata/sensai-dataset/blob/master/LICENSE)
- Dataset: [ODC Public Domain Dedication and Licence (PDDL)](https://opendatacommons.org/licenses/pddl/1-0/index.html)
