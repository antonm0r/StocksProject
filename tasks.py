# tasks.py
from crewai import Task
from textwrap import dedent


class StockAnalysisTasks:
    def __tip_section(self):
        return "If you do your BEST WORK and return exactly what I ask, I'll give you a $10,000 commission!"

    def search_news(self, agent, data: str):
        return Task(
               description=dedent(f"""
            **Task**: Search for the latest news related to a specified company.
            **Description**: Use News Search Tool to get latest news about the company.

            **Parameters**: 
            - Company: {data}

            **Notes**
            {self.__tip_section()}
            """
        ),
            agent=agent,
            expected_output="""List of key news articles with links and snippets."""
        )

    def get_data_from_api(self, agent, data: str):
        return Task(
            description=dedent(f"""
            **Description**: Get detailed stock data using AlphaVantage API.

            **Notes**
            You MUST use AlphaVantageTool to dynamically retrieve all available metrics for the {data} stock SYMBOL.
            This tool automatically extracts every data point returned by the API.
            {self.__tip_section()}
            """
             ),
            agent=agent,
            expected_output=dedent("""
            A list of all FINANCIAL metrics and the data retrieved for each one. 
            Example output: [
                {'metric': 'PERatio', 'data': 'some_value'},
                {'metric': '52WeekHigh', 'data': 'some_value'},
                ... (all other FINANCIAL metrics available)
            ]""")
        )

    def create_report(self, agent, news_context, data_context) -> Task:
        return Task(
            description=dedent(f"""
            Analyze the news and stock data fetched in previous tasks to create a comprehensive investment report.

            {self.__tip_section()}
            """),
            agent=agent,
            context=[news_context[0], data_context[0]],
            expected_output="""
                A synthesized report detailing the company's performance,
                market trends, and news sentiment analysis.
                """
        )



