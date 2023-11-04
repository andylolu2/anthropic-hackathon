from dotenv import load_dotenv
from langchain.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate

from custom_parser import MarkdownOutputParser

load_dotenv()

model = ChatAnthropic(max_tokens=10_000)


def ask_claude(query: str, answer_beginning: str = ""):
    prompt = PromptTemplate(
        template="""
        
        Human:
        {query}
        Assistant:
        {answer_beginning}""",
        input_variables=["query", "answer_beginning"],
    )

    chain = prompt | model
    return chain.invoke({"query": query, "answer_beginning": answer_beginning}).content


def ask_claude_md(query: str):
    parser = MarkdownOutputParser()
    prompt = PromptTemplate(
        template="""
        
        Human:
        {query}
        {format_instructions}
        Assistant:
        """,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser
    return chain.invoke({"query": query})
