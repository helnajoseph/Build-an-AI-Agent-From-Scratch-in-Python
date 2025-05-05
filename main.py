from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


llm = ChatOpenAI(model="gpt-3.5-turbo")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})

try:
    # The output is a JSON string, not a list of dictionaries
    output = raw_response.get("output")
    structured_response = parser.parse(output)

    # Print the response in a more readable format
    print("\n=== Research Results ===")
    print(f"Topic: {structured_response.topic}")
    print(f"Summary: {structured_response.summary}")
    print(f"Sources: {', '.join(structured_response.sources) if structured_response.sources else 'None'}")
    print(f"Tools Used: {', '.join(structured_response.tools_used) if structured_response.tools_used else 'None'}")
    print("======================\n")

    # Optionally save the results
    save_result = input("Would you like to save these results? (y/n): ")
    if save_result.lower() == 'y':
        save_tool.run(str(structured_response))
        print("Results saved successfully!")

except Exception as e:
    print("Error parsing response:", e)
    print("Raw Response:", raw_response)