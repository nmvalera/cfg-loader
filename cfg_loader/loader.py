"""
    cfg_loader.loader
    ~~~~~~~~~~~~~~~~~

    Implement the loading class

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import os

from .exceptions import ConfigFileMissingError, ConfigFileNotFoundError
from .utils import parse_yaml_file

# Default environment variable containing the path of a .yaml configuration file
DEFAULT_CONFIG_FILE_ENV_VAR = 'CONFIG_FILE'


class BaseConfigLoader:
    """Base config loader using a marshmallow schema to validate and process input data

    :param schema: Marshmallow schema used to deserialize configuration input data
    """

    def __init__(self, config_schema, substitution_mapping=None):
        self.substitution_mapping = substitution_mapping or {}
        self.config_schema = config_schema

    def load(self, data, substitution_mapping=None):
        """Load configuration from an object

        :param input: Data to load configuration from (must be deserializable by schema)
        :type input: object
        """
        substitution_mapping = substitution_mapping or self.substitution_mapping

        return self.config_schema(substitution_mapping=substitution_mapping).load(data)


class YamlConfigLoader(BaseConfigLoader):
    """Config loader that reads config from .yaml file

    :param config_file_env_var: Environment variable to read config file path from if not provided when loading
    :type config_file_env_var: str
    :param default_config_path: Used if neither path is provided at loading nor environment variable
    :type default_config_path: str
    """

    def __init__(self, *args, config_file_env_var=DEFAULT_CONFIG_FILE_ENV_VAR, default_config_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file_env_var = config_file_env_var
        self.default_config_path = default_config_path

    def check_file(self, config_file):
        """Check file validity

        :param config_file: Path to the .yaml configuration file
        :type config_file: str
        """

        if config_file is None:
            raise ConfigFileMissingError("""
                    No configuration file specified.
                    Please provide a configuration valid file path or
                    set the environ variable '{var}'
                """.format(var=self.config_file_env_var))

        if not os.path.isfile(config_file):
            raise ConfigFileNotFoundError("""
                    No such file '{path}'
                """.format(path=config_file))

        return config_file

    def load(self, config_file=None, substitution_mapping=None):
        """Load configuration from .yaml file

        :param config_file: Path to the .yaml configuration file
        :type config_file: str
        """

        config_file = config_file or os.environ.get(self.config_file_env_var) or self.default_config_path

        # Check config_file is valid
        self.check_file(config_file)

        # Parse yaml file
        data = parse_yaml_file(config_file)

        return super().load(data, substitution_mapping)
