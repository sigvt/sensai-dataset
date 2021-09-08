from datasets.features import ClassLabel, Features, Value
from datasets.load import load_dataset


def load_sensai_dataset():
    dataset = load_dataset(
        "holodata/sensai",
        features=Features({
            "body": Value("string"),
            "toxic": ClassLabel(num_classes=2, names=['0', '1'])
        }))
    dataset = dataset['train']
    return dataset
