all: build

build:
	python3 -m sensai_dataset.generator

upload:
	kaggle datasets version -m "New version" --path $$DATASET_DIR
