import json

class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = None  # 初期値はNoneにしておく
        self.loop_count = None
        self.initial_message = None
        self.steps = None
        self.comparison_region = None
        self.standby_position = None
        self.comparison_threshold = None
        self.retry_delay_seconds = None
        self.post_sequence_delay_seconds = None
        self.screen_verification_enabled = None

    def load_config(self):
        try:
            with open(self.file_path, 'r') as file:
                config = json.load(file)
                self.validate_config(config)
                self.loop_count = config.get("loop_count", 1)  # デフォルトでは1回
                self.initial_message = config.get("initial_message", "")
                self.steps = config.get("steps", [])
                self.comparison_region = config.get("comparison_region", None)
                self.standby_position = config.get("standby_position", {"x": 100, "y": 100})
                self.comparison_threshold = config.get("comparison_threshold", 0.95)
                self.retry_delay_seconds = config.get("retry_delay_seconds", 5)
                self.post_sequence_delay_seconds = config.get("post_sequence_delay_seconds", 5)
                # 画面照合を使わず steps だけをループしたい場合は "screen_verification": false を指定する。
                # 未指定のときは comparison_region の有無で自動的に決まる（後方互換）。
                self.screen_verification_enabled = self.resolve_screen_verification(config)
                self.config = config
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Error loading configuration from {self.file_path}: {e}")

    def validate_config(self, config):
        if "steps" not in config:
            raise ValueError("'steps' key is missing in the configuration.")

    def resolve_screen_verification(self, config):
        has_region = self.comparison_region is not None
        enabled = config.get("screen_verification", has_region)

        if not isinstance(enabled, bool):
            raise ValueError("'screen_verification' must be a boolean value.")
        if enabled and not has_region:
            raise ValueError(
                "'screen_verification' is enabled but 'comparison_region' is missing."
            )
        return enabled
    
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

    def get_comparison_region(self):
        if self.config is None:
            self.load_config()
        return self.comparison_region

    def get_standby_position(self):
        if self.config is None:
            self.load_config()
        return self.standby_position

    def get_comparison_threshold(self):
        if self.config is None:
            self.load_config()
        return self.comparison_threshold

    def get_retry_delay_seconds(self):
        if self.config is None:
            self.load_config()
        return self.retry_delay_seconds

    def get_post_sequence_delay_seconds(self):
        if self.config is None:
            self.load_config()
        return self.post_sequence_delay_seconds

    def is_screen_verification_enabled(self):
        if self.config is None:
            self.load_config()
        return self.screen_verification_enabled
