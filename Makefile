all: build upload

build:
	python3 -m sensai_dataset.gen

upload:
	kaggle datasets version -m "New version" --path $$DATASET_DIR
