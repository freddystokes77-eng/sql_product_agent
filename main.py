from openai import OpenAI
from dotenv import load_dotenv
from agents import Runner
import asyncio
from custom_agents.product_agent import agent_1

load_dotenv()  # Load environment variables from .env file

client = OpenAI()

# Function to run the agent in a loop, taking user input and generating responses until the user exits
async def main():

    agent = agent_1

    conversation = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        conversation.append({
            "role": "user",
            "content": user_input
        })

        result = await Runner.run(agent, conversation)

        response = result.final_output

        print("Assistant:", response)

        conversation.append({
            "role": "assistant",
            "content": response
        })

asyncio.run(main())

