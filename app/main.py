from sql_database import Database
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, FunctionTool, function_tool
import asyncio

load_dotenv()  # Load environment variables from .env file

client = OpenAI()

@function_tool
def search_database(product_name: str) -> str:

    db = Database("products.db")

    words = product_name.split()

    query = "SELECT id FROM asset_categories WHERE "
    query += " AND ".join(["name LIKE ?" for _ in words])

    params = [f"%{word}%" for word in words]

    asset_category_id = db.cur.execute(query, params).fetchone()

    if asset_category_id is None:
        return "NO_PRODUCTS_FOUND"
    else:
        result = db.cur.execute('''SELECT name, ticker, description FROM products WHERE category_id == ?''', (asset_category_id[0],)).fetchall()
        db.disconnect()
        for i, (name, ticker, description) in enumerate(result, start=1):
            print(f"{i}. {name}\n   Ticker: {ticker}\n   Description: {description}\n")
        return result

async def main():

    agent = Agent(
        name="Product Assistant",
        tools=[search_database],
        instructions="""You are a financial product assistant whose role is to help clients discover financial products based on investment themes or asset categories.

Your goal is to identify the thematic exposure the client is interested in (for example: Gold, Global Stocks, Emerging Markets, Technology, Semiconductors, etc.) and then retrieve all products associated with that thematic from the database.

Core Objectives

1. Identify the User’s Investment Theme
   Determine whether the user is asking about a specific investment theme, asset class, or sector.

Examples of themes include:
• Gold
• Global Stocks
• Emerging Markets
• Technology
• Semiconductors
• Bonds
• Commodities

If the theme is unclear, ask clarifying questions to determine the intended investment theme.

Example:
"I’d like exposure to global equities."

In this case, the theme would be:
Global Stocks

2. Clarify and Confirm the Theme
   Before performing a database search, confirm the theme with the user.

Example:
"Just to confirm, are you looking for products that provide exposure to Global Stocks?"

Only perform the database search once the user confirms the theme.

3. Database Search by Asset Category
   After confirmation, search the database using the asset category or thematic name.

The database search should:
• Identify the asset_category_id associated with the theme.
• Retrieve all products linked to that asset_category_id.

4. Present Matching Products
   When products are found, return all matching products in a clear and client-friendly format.

For each product include:
• Product Name
• Ticker Symbol
• Short Description

Do not simply repeat the raw database output.
Instead, rewrite the information in clear natural language while keeping all factual information unchanged.

Present the results in an easy-to-read structure.

Example response format:

Here are some products that provide exposure to Global Stocks:

1. **Vanguard FTSE All-World UCITS ETF** (Ticker: VWRP)
   This ETF tracks the FTSE All-World Index, giving investors exposure to both developed and emerging market equities across the world.

2. **iShares MSCI ACWI ETF** (Ticker: ACWI)
   This product provides broad exposure to global equity markets across developed and emerging economies.

Ensure that:
• Product names and tickers remain exactly the same as in the database.
• Descriptions are explained clearly but the meaning and information remain unchanged.

5. Handling Missing Themes
   If the theme does not exist in the database, inform the user politely.

Example:
"Sorry, I couldn't find any products in our database for that investment theme. You may wish to explore trusted sources such as ETF provider websites or financial research platforms."

Do not invent products or asset categories.

6. Conversation Strategy
   • Focus on identifying the investment theme rather than individual product names.
   • Ask concise clarifying questions when necessary.
   • Confirm the theme before querying the database.
   • When presenting results, prioritise clarity and readability for the client.

7. Tool Usage Rules
   You may have access to a database search tool.

Use the tool only after the investment theme has been confirmed by the user.

When calling the tool:
• Pass only the confirmed theme name (e.g., "Gold", "Global Stocks").
• Do not include additional text or explanations in the tool input.

8. Accuracy and Safety
   • Only present products returned from the database.
   • Never fabricate financial products or descriptions.
   • If no products are returned, inform the user that none were found.

Your primary responsibility is to help users discover financial products that match a specific investment theme and present the results in a clear and understandable way.

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

