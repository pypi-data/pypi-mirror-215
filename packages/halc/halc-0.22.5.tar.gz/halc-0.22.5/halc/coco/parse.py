"""
Create a methods for parsing COCO annotations and creating a dataset.
"""
import json


class COCO:
    def __init__(self, path: str):
        self.path = path
        self.dataset = self.load_dataset(self.path)

    def load_dataset(self, path: str):
        with open(path) as f:
            dataset = json.load(f)
        return dataset