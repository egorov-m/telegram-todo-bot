import os
import json
import logging.config


def setup_logging(
        default_path='./src/logging.json',
        default_level=logging.INFO,
        LOG_CFG='LOG_CFG'
):
    """
    Setup logging configuration
    """

    path = default_path
    log_config = os.getenv(LOG_CFG, None)
    if log_config:
        path = log_config
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
