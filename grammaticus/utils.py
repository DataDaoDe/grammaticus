import os

PROJECT_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__))
)

DATA_DIR = os.path.join(PROJECT_DIR, 'data')


def data_filepath(filepath: str) -> str:
    return os.path.join(DATA_DIR, filepath)
