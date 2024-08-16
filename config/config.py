import json

class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = None  # 初期値はNoneにしておく
        self.loop_count = None
        self.initial_message = None
        self.steps = None

    def load_config(self):
        try:
            with open(self.file_path, 'r') as file:
                config = json.load(file)
                self.validate_config(config)
                self.loop_count = config.get("loop_count", 1)  # デフォルトでは1回
                self.initial_message = config.get("initial_message", "")
                self.steps = sorted(config.get("steps", []), key=lambda x: x.get("index", float('inf')))
                self.config = config
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Error loading configuration from {self.file_path}: {e}")

    def validate_config(self, config):
        if "steps" not in config:
            raise ValueError("'steps' key is missing in the configuration.")
        for click_config in config["steps"]:
            if 'index' not in click_config:
                raise ValueError("'index' key is missing in one of the steps.")
    
    def get_loop_count(self):
        if self.config is None:
            self.load_config()
        return self.loop_count

    def get_initial_message(self):
        if self.config is None:
            self.load_config()
        return self.initial_message

    def get_steps(self):
        if self.config is None:
            self.load_config()
        return self.steps