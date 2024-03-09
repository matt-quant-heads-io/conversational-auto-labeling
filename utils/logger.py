import logging.config
import yaml

with open("configs/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    logging.captureWarnings(True)


def get_logger(name: str):
    """Logs a message
    Args:
    name(str): name of logger
    """
    logger = logging.getLogger(name)
    return logger


def init_logger(log_name="main"):
    log_root = pathlib.Path(__file__).parent.resolve()
    log_file = f"{log_root}/{log_name}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s> %(funcName)s::%(filename)s::%(lineno)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )
