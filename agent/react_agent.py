from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from agent.tools.agent_tools import (rag_summarize, get_weather, get_user_location, get_user_id,
                                     get_current_month, fetch_external_data, fill_context_for_report)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch

from utils.prompt_uploader import load_system_prompts, load_report_prompts



class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model = ChatOpenAI(model="gpt-5-nano", temperature=0),
            tools=[rag_summarize, get_weather, get_user_location, get_user_id,
                   get_current_month, fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
            system_prompt = load_system_prompts()
        )

    def execute_stream(self, query:str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }

        for chunk in self.agent.stream(input_dict, stream_mode = 'values', context = {"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()

    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
