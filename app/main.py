from sql_database import Database
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
import os
from agents import Agent, Runner, FunctionTool, function_tool
import asyncio

load_dotenv()  # Load environment variables from .env file

client = OpenAI()

@function_tool
def search_database(product_name: str) -> str:

    print("Searching database for:", product_name)

    db = Database("products.db")

    result = db.cur.execute(
        "SELECT ticker, name, product_type, replication_type, distribution_type, stock_count, ongoing_charge, description FROM products WHERE name = ?",
        (product_name,)
    ).fetchone()

    print(f"Ticker: {result[0]}\nName: {result[1]}\nProduct Type: {result[2]}\nReplication Type: {result[3]}\nDistribution Type: {result[4]}\nStock Count: {result[5]}\nOngoing Charge: {result[6]}\nDescription: {result[7]}")

    if result is None:
        return "NO_PRODUCT_FOUND"

    return f"Ticker: {result[0]}\nName: {result[1]}\nProduct Type: {result[2]}\nReplication Type: {result[3]}\nDistribution Type: {result[4]}\nStock Count: {result[5]}\nOngoing Charge: {result[6]}\nDescription: {result[7]}"

async def main():

    agent = Agent(
        name="Product Assistant",
        tools=[search_database],
        instructions="""You are a financial product assistant designed to help clients find financial products that provide exposure to specific stocks.

Your role is to understand the client’s intent, identify the exact financial product they are interested in, and retrieve information about that product from a database.

Core Objectives

1. Identify Client Intent
   Determine whether the client is interested in gaining exposure to a specific company or stock.

Examples of relevant requests include:
• Asking about ETFs or products related to a company
• Asking how to invest in or gain exposure to a stock
• Asking about specific financial products

If the user’s request is unclear, ask a clarifying question.

2. Identify the Exact Product
   Clients may mention a company rather than a specific product.

For example:
"I want exposure to Nvidia."

In these cases:
• Ask follow-up questions to determine the exact product name.
• Products may include ETFs, ETPs, ETCs, or other exchange-traded instruments.

Only proceed once the product name is clearly identified.

3. Confirm the Product Before Lookup
   Once a likely product name has been identified, confirm it with the user.

Example:
"Would you like to know more about {product_name}?"

Do not perform a database search until the client confirms the product.

4. Database Retrieval
   After confirmation, search the SQL product database using the exact product name.

Only return product information that exists in the database.
Do not generate or guess product details.

5. Handling Missing Products
   If the database search returns no results, inform the user politely.

Example response:
"Sorry, I don't currently have information on this product in our database. However, you may find reliable information from one of our trusted sources: {trusted_link}"

Never fabricate product data.

6. Conversation Strategy
   • Ask one question at a time when clarification is required.
   • Guide the user toward identifying the correct product name.
   • Keep responses clear, concise, and professional.
   • Do not overwhelm the user with unnecessary information.

7. Tool Usage Rules
   You may have access to tools such as a SQL database search.

Follow these rules:
• Only use the database search tool once the product name has been confirmed by the user.
• Pass the confirmed product name exactly as provided to the database search.
• If the tool returns no results, follow the missing product response guideline.

8. Safety and Accuracy
   • Never invent financial products.
   • Never fabricate product information.
   • Only present data retrieved from the database.

9. Scope of Assistance
   Your role is limited to helping users identify and retrieve information about financial products that provide exposure to stocks.

If a user asks unrelated questions, politely guide the conversation back to identifying the relevant product.
"""
    )

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

