from loguru import logger
from rich.console import Console
import sys

console = Console()

logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
)

logger.add(
    "outputs/reports/deep_research.log",
    rotation="10 MB",
    retention=5,
    level="INFO",
)

__all__ = ["logger", "console"]