import logging
import pathlib
import sys


def init_logger(log_name: str = "main", log_root_path: str = None):
    """
    Description of init_logger

    Args:
        log_name="main" (undefined):
        log_root_path=None (undefined):

    """
    log_root = log_root_path or pathlib.Path(__file__).parent.resolve()
    log_file = f"{log_root}/{log_name}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s> %(funcName)s::%(filename)s::%(lineno)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )
