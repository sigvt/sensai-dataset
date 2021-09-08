# Contribution Guide

## Setup

```bash
poetry install
```

## Generate dataset

```bash
python3 -m sensai_gen.cli -m 'chats_2021-*'
```

## Upload new version of dataset (Maintainers only)

```bash
make upload
```
