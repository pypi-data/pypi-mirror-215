import uuid
from loguru import logger
from langchain.llms.base import BaseLLM
from langchain.agents import initialize_agent, AgentType
from .get_integrations import get_apis_from_env
from .cito_api_wrapper import CitoAPIWrapper
from .cito_toolkit import CitoToolkit

def create_workflow(llm: BaseLLM):

    logfile_path = "output.log"
    logger.remove(handler_id=None)
    logger.add(logfile_path, format="{time} - {extra[session_id]} - {extra[operation_name]} - {message}")

    tools_dict = get_apis_from_env()
    session_id = uuid.uuid4()

    cito_wrapper = CitoAPIWrapper()
    toolkit = CitoToolkit.from_cito_api_wrapper(cito_wrapper, tools_dict, logger, str(session_id))
    tools = toolkit.get_tools()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True
    )

    prompt = input("Enter your task: ") + ". Give your action input in a JSON format where the keys are the params \
        and the values are the value for each input parameter. Your final answer should summarise what you did and the result."
    answer = agent.run(prompt)

    logger.remove()
    logger.add(logfile_path, format="{time} - {extra[session_id]} - {message}")
    logger.bind(session_id=session_id).info(answer)