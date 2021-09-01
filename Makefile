all: build upload

build:
	python3 -m sensai_gen.cli

upload:
	kaggle datasets version -d -m "New version" --path $$DATASET_DIR
