import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import get_releases, get_commits
from langchain.messages import HumanMessage

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

def main():
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-120b"
    )

    simple_agent = create_agent(
        model=llm,
        tools=[get_releases, get_commits],
        system_prompt="You're a helpful assistant that can fetch GitHub repository releases and commits."
    )

    messages = []

    while True:
        user_input = input("Enter your query (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        messages.append(HumanMessage(content=user_input))
        response = simple_agent.invoke({
            "messages": messages,
        })
        messages.append(response["messages"][-1])
        print(f"Agent Response:\n{response["messages"][-1].content}\n")

if __name__ == "__main__":
    main()