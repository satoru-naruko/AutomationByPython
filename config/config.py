import json

class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = None  # 初期値はNoneにしておく

    def load_config(self):
        try:
            with open(self.file_path, 'r') as file:
                config = json.load(file)
                self.validate_config(config)
                self.config = sorted(config, key=lambda x: x.get("index", float('inf')))
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Error loading configuration from {self.file_path}: {e}")

    def validate_config(self, config):
        for click_config in config:
            if 'index' not in click_config:
                raise ValueError("'index' key is missing in the configuration.")

    def get_config(self):
        if self.config is None:
            self.load_config()
        return self.config