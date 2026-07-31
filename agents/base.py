from core.llm import get_llm
from core.logger import logger


class BaseAgent:
    """
    Base class for all LLM-powered agents.
    """

    def __init__(self):
        self.llm = get_llm()
        self.logger = logger