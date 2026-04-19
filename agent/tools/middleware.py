from typing import Callable

from utils.logger_handler import logger
from utils.prompt_uploader import load_report_prompts, load_system_prompts

from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage

from langchain.agents.middleware import ModelRequest, before_model, dynamic_prompt, wrap_tool_call
from langchain.agents import AgentState

from langgraph.types import Command
from langgraph.runtime import Runtime


# To monitor the tool usage
@wrap_tool_call
def monitor_tool(request: ToolCallRequest,
                 handler: Callable[[ToolCallRequest], ToolMessage | Command]) -> ToolMessage | Command:
    # request contains the tool call information, including the tool name and input arguments
    # handler is the function that will execute the tool call and return the result

    logger.info(f"[Tool Monitor] Tool {request.tool_call['name']} is being called")
    logger.info(f"[Tool Monitor] Input: {request.tool_call['args']}")

    # handler(request) will execute the tool call and return the result, which can be a ToolMessage or a Command
    try:
        response = handler(request)
        logger.info(f"[Tool Monitor] Tool {request.tool_call['name']} executed successfully")

        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return response
    except Exception as e:
        logger.error(f"[Tool Monitor] Tool {request.tool_call['name']} execution failed: {str(e)}")
        raise e

# To keep a record in log before running the model 
@before_model
def log_before_model(
        state: AgentState,  # Record the state of the agent
        runtime: Runtime # Metadata about the current execution environment/invocation.
):
    logger.info(f"[Model Monitor] Agent state: {state}")
    logger.info(f"[Model Monitor] Runtime information: {runtime}")

# To dynamically switch the prompt based on the context
# Dynamic_prompt is a middleware decorator lets you modify the messages (prompt) sent to 
# the LLM on every model call, right before invocation.
@dynamic_prompt
def report_prompt_switch(
    request:ModelRequest):
    # Flag for switching to report prompt:
    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompts()
    
    return load_system_prompts()