# from dotenv import load_dotenv
# from langchain.chat_models import ChatAnthropic
# from langchain.prompts import ChatPromptTemplate

# load_dotenv()

# model = ChatAnthropic()

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("human", "Tell me a joke about {topic}"),
#     ]
# )

# chain = prompt | model

# prompt_value = prompt.format_prompt(topic="bears")
# prompt = model.convert_prompt(prompt_value)
# print(prompt)

# out = chain.invoke({"topic": "bears"})

# print(out)

import requests
from bs4 import BeautifulSoup, Comment

url = "https://cks.nice.org.uk/topics/osteoporosis-prevention-of-fragility-fractures/"

response = requests.get(url)


def clean_html(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # remove all scripts, styles, headers, navigation, footer, svg paths
    for script in soup(["script", "style", "nav", "path"]):
        script.extract()

    for comment in soup.findAll(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # get the roughly-cleaned html
    small_html = str(soup.prettify())

    return small_html


print(clean_html(response.text))
