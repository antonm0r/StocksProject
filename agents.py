# agents.py
from crewai import Agent
from textwrap import dedent

from tools import SearchTools, AlphaVantageTool
from dotenv import load_dotenv

load_dotenv()


class FinancialResearchAgents:
    def news_agent(self):
        return Agent(
            role="News Analyst",
            goal=dedent(f"""Retrieve relevant news for a given company."""),
            backstory=dedent(
                f"""Expert in getting relevant news. The best at using tools to search for news."""),
            tools=[
                SearchTools(),
            ],
            verbose=True,
        )

    def data_agent(self):
        return Agent(
            role="Data Analyst",
            goal=dedent(f"""Retrieve relevant data using the tool."""),
            backstory=dedent(
                f"""Expert in getting data from API."""),
            tools=[
                AlphaVantageTool()
            ],
            verbose=True,
        )

    def report_agent(self):
        return Agent(
            role="Investment Strategist",
            goal=dedent(f"""Synthesize context from multiple sources to prepare a detailed investment report."""),
            backstory=dedent(
                f"""An experienced strategist with a knack for combining various data into 
                cohesive, actionable investment advice."""),
            allow_delegation=False,
            verbose=True,
        )


