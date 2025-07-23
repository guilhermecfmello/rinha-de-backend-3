import logging
from dotenv import load_dotenv
load_dotenv()
from src.services import get_worker_service
from src.services.worker_service import WorkerService

from config import Config
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting worker service...")
    worker: WorkerService = get_worker_service()
    worker.process_queue()
