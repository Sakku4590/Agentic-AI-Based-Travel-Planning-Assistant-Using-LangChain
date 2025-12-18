import json
from utils.logger import get_logger

logger = get_logger(__name__)

def load_json(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
        logger.info(f"Loaded data from {path}")
        return data
    except Exception as e:
        logger.error(f"Failed to load {path}: {e}")
        raise