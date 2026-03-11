from agents import Agent
from prompts.product_agent_prompt import PRODUCT_AGENT_PROMPT
from tools.database_tools import search_database

agent_1 = Agent(
        name="Product Assistant",
        tools=[search_database],
        instructions=PRODUCT_AGENT_PROMPT)