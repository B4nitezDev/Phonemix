import yaml

class Config:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)
            
phonemize_config = Config('config/phonemize_config.yml').config
