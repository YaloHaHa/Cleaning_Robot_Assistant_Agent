
import os
import random
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010",]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

external_data = {}
rag_service = RagSummarizeService()

@tool(description="Use this tool to summarize a query using RAG. Input should be a natural language query string. Output will be a concise summary based on the retrieved relevant documents.")
def rag_summarize(query:str) -> str:
    return rag_service.rag_summarize(query)

@tool(description="Use this tool to get the current weather for a specified city. Input should be the name of the city as a string. Output will be a brief weather report for that city.")
def get_weather(city:str) -> str:
    # Placeholder for a weather API call
    return f"The current weather in {city} is sunny with a high of 25°C."

@tool(description="Use this tool to get the user's current location. Input should be empty. Output will be the name of the city where the user is currently located.")
def get_user_location() -> str:
    # Placeholder for a function that retrieves the user's location
    return random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"])

@tool(description="Use this tool to get the current date and time. Input should be empty. Output will be the current date and time in ISO format.")
def get_user_id() -> str:
    return random.choice(user_ids)

@tool(description="Use this tool to get the current month. Input should be empty. Output will be the current month in YYYY-MM format.")
def get_current_month() -> str:
    return random.choice(month_arr)

# Load and parse external CSV data into the global `external_data` dict (lazily initialized).
# The CSV is expected to have columns: user_id, feature, efficiency, consumables, comparison, time.
# Data is structured as: external_data[user_id][time] = {feature, efficiency, consumables, comparison}
# Other tools can then look up per-user, per-month records directly from `external_data`.
def generate_external_data():
    if not external_data:
        external_path = get_abs_path(agent_conf["external_data_path"])
        if not os.path.exists(external_path):
            raise FileNotFoundError(f"External data file not found at {external_path}")
        with open(external_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:  # Skip header line
                arr: list[str] = line.strip().split(",")
                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}
                external_data[user_id][time] = {
                    "feature": feature,
                    "efficiency": efficiency,
                    "consumables": consumables,
                    "comparison": comparison,
                }

@tool(description="Use this tool to fetch external data for a specific user and month. Input should be a string with 'user_id' and 'month' fields. Output will be the corresponding data record for that user and month, or an empty string if not found.")
def fetch_external_data(user_id: str, month: str) -> dict:
    generate_external_data()
    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"No external data found for user_id={user_id} and month={month}")
        return("")      

@tool(description="Use this tool to fill in the context for a report. Input should be empty. Output will be a string indicating that the context has been filled.")
def fill_context_for_report():
    return "fill_context_for_report tool called."