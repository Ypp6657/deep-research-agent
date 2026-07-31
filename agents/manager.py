from agents.planner import PlannerAgent
from agents.search import SearchAgent
from agents.summarizer import SummarizerAgent
from agents.critic import CriticAgent
from agents.writer import WriterAgent

from core.logger import logger
from core.schemas import FinalReport


class ResearchManager:

    def __init__(self):

        self.planner = PlannerAgent()
        self.search = SearchAgent()
        self.summarizer = SummarizerAgent()
        self.critic = CriticAgent()
        self.writer = WriterAgent()

    def run(
        self,
        query: str,
    ) -> tuple[FinalReport, bool]:

        logger.info("Planning research...")

        plan = self.planner.plan(query)

        logger.info("Searching web...")

        results = self.search.search(plan)

        logger.info("Summarizing search results...")

        summaries = self.summarizer.summarize(results)

        logger.info("Reviewing research quality...")

        review = self.critic.review(
            query,
            summaries,
        )

        logger.info(
            f"Research Complete: {review.is_complete}"
        )

        logger.info("Generating final report...")

        report = self.writer.write(
            query,
            summaries,
        )

        return report, review.is_complete