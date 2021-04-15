class DatabaseConnection:
    def __init__(self):
        self.config = get_config()
        self.host = self.config['database_host']
        self.username = self.config['database_username']
        self.schema = self.config['database_schema']
        self.password = self.config['database_password']

    def get_config():
        with open('config.json', 'r') as input_file:
            config_data = json.load(input_file)

        return config_data
