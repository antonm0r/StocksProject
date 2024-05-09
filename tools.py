# tools.py
from crewai_tools import BaseTool
import os
import requests

class SearchTools(BaseTool):
    name: str = "News Search Tool"
    description: str = "Searches for news about a company, stock, or any other topic and returns relevant results."

    def _run(self, query: str) -> str:
        top_result_to_return = 10
        url = "https://google.serper.dev/news"
        payload = {"q": query}
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY', 'default-api-key'),
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            results = response.json().get('news', [])
            string = []
            for result in results[:top_result_to_return]:
                title = result.get('title', 'No title available')
                link = result.get('link', 'No link available')
                snippet = result.get('snippet', 'No snippet available')
                string.append('\n'.join([
                    f"Title: {title}",
                    f"Link: {link}",
                    f"Snippet: {snippet}",
                    "\n-----------------"
                ]))
        except Exception as e:
            return f"An error occurred: {e}"
        return '\n'.join(string)



class AlphaVantageTool(BaseTool):
    name: str = "AlphaVantage API Tool"
    description: str = """
        Useful to search company overview information for a given stock.
        The input to this tool should be the stock ticker you are interested in.
        For example, `AAPL`.
        """

    def _run(self, company_symbol: str) -> list:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={company_symbol}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        # Define financial metrics keys
        financial_keys = {'MarketCapitalization', 'EBITDA', 'PERatio', 'PEGRatio', 'BookValue',
                          'EPS', 'RevenuePerShareTTM', 'ProfitMargin', 'OperatingMarginTTM',
                          'ReturnOnAssetsTTM', 'ReturnOnEquityTTM', 'RevenueTTM', 'GrossProfitTTM',
                          'QuarterlyEarningsGrowthYOY', 'QuarterlyRevenueGrowthYOY', 'AnalystTargetPrice',
                          'TrailingPE', 'ForwardPE', 'PriceToSalesRatioTTM', 'PriceToBookRatio',
                          'EVToRevenue', 'EVToEBITDA'}

        # Filter and process the data to fit the expected output format
        processed_data = []
        for key, value in data.items():
            if key in financial_keys:
                processed_data.append({'metric': key, 'data': value})

        return processed_data



