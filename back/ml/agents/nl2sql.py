import sys
from pathlib import Path 

from app.config import settings

sys.path.append(str(Path(__file__).parent.parent))

from main import *

from langchain_openai import ChatOpenAI
def create_generator(gen_kwargs=None):
    return ChatOpenAI(
        api_key="EMPTY",
        model="Qwen/Qwen2.5-32B-Instruct-AWQ", 
        openai_api_base="http://192.168.1.2:8000/v1",  
        timeout=600,
        temperature=0,
        **(gen_kwargs or {}) 
    )


qwen = create_generator()

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import SQLDatabase

db = SQLDatabase.from_uri(
    database_uri=settings.get_db_url(),
    # database_uri="postgresql://mireahack:root@postgres:5432/mireahack",
    schema="public"
)

from main import llm

prompt = """             
    Answer the following questions as best you can. You have access to the following tools:

    sql_db_query - Input to this tool is a detailed and correct SQL query, output is a result from the database. 
    If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, 
    and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.
    sql_db_schema - Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables. 
    Be sure that the tables actually exist by calling sql_db_list_tables first! Example Input: table1, table2, table3
    sql_db_list_tables - Input is an empty string, output is a comma-separated list of tables in the database.
    sql_db_query_checker - Use this tool to double check if your query is correct before executing it. Always use this tool 
    before executing a query with sql_db_query!

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [sql_db_query, sql_db_schema, sql_db_list_tables, sql_db_query_checker] 
    Action Input: the input to the action (Never enclose SQL in ``` marks to avoid errors, at the end of any query insert ";")
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Check the format again! It’s extremely important to follow it correctly.


    You are an expert SQL analyst with deep knowledge of database optimization. Follow these rules strictly:

    1. Examine the DB schema - use only specified tables and fields
    2. Queries must be maximally efficient (use proper indexes, JOINs)
    3. For complex queries, add comments explaining the logic
    4. Avoid SELECT * - specify only needed fields
    5. For analytical queries, propose multiple options with performance estimates
    6. Ask clarifying questions if requirements are ambiguous
    7. Format queries for readability (line breaks, indentation)
    8. Never enclose SQL in ``` marks to avoid errors
    9. If data cannot be found, reply "No data"
    10. Omit municipalities with missing data entirely
    11. Respond in Russian
    12. You earn $200 for each correct query
    13. Limit results to 10 examples max (LIMIT 10)
    14. Verify query accuracy before submitting
    16. When calculating the population, be sure to indicate that this is the agglomeration population.
    17. Never use filtering by “All” under any circumstances.
    18. If the user has not specified a time period, use the entire period from January 2023 through December 2024 to retrieve the information.
    19. Be sure to mention the year or time period, as well as the metrics of the examples provided.
    20. When indicating average consumer spending, specify that these figures represent average cashless spending per ONE person.
    21. Do not sum the consumer expenditures; instead, calculate the average value for each municipality.
    22. Search for the names of municipalities in the municipal_districts table.

    Database Specifications:
    1. Market Accessibility Index shows relative external market potential (higher = more promising)
    2. For salary data, ONLY use value in bdmo_salary (average monthly salary in RUB)
    3. Connection table:
    - territory_id_x: Departure MO code
    - territory_id_y: Arrival MO code
    - distance: Distance in km (as of 12/31/2024)
    - Note: Distances are one-way (x→y) assuming return path is identical
    4. Years: 2023 and 2024
    5. Consumption - stimation of average cashless consumer spending in the current month by residents of the municipality
    based on SberIndex models using transaction data (RUB) (higher = more promising). If data is missing, the estimate does not meet the required quality threshold.


    Current task: {input}
    Thought process: {agent_scratchpad}
"""


toolkit = SQLDatabaseToolkit(db=db, llm=qwen)
sql_agent = initialize_agent(
    llm=qwen, 
    tools=toolkit.get_tools(),
    handle_parsing_errors=True,
    verbose=True
)

sql_agent.agent.llm_chain.prompt.template = prompt

def nl2sql_agent(state: State):

    query = state['messages'][-1]['content']

    result = sql_agent.run({f"""input': {query}
    """})

    return {'nl2sql_context':result}
