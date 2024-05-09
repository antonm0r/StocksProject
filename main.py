# main.py
from crewai import Crew

from textwrap import dedent
from agents import FinancialResearchAgents
from tasks import StockAnalysisTasks

class FinancialCrew:
    def __init__(self, data):
        self.data = data

    def run(self):
        agents = FinancialResearchAgents()
        tasks = StockAnalysisTasks()

        # AGENTS
        news_agent = agents.news_agent()
        data_agent = agents.data_agent()
        report_agent = agents.report_agent()

        # TASKS
        search_news = tasks.search_news(news_agent, self.data)
        get_stock_data = tasks.get_data_from_api(data_agent, self.data)
        create_report = tasks.create_report(report_agent, [search_news], [get_stock_data])

        # CREW
        crew = Crew(
            agents=[
                news_agent,
                data_agent,
                report_agent
                ],
            tasks=[
                search_news,
                get_stock_data,
                create_report,
                ],
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to Report Creator Crew")
    print("-------------------------------")
    data = input(dedent("""Enter company name you want to get report for:\n>> """))

    mycrew = FinancialCrew(data)
    result = mycrew.run()
    print("\n\n########################")
    print("## Here is your result:")
    print("########################\n")
    print(result)



