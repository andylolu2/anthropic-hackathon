import json
import re

from langchain.prompts import PromptTemplate, StringPromptTemplate
import time
from langchain.chains import ConversationChain
import torch
from langchain.chat_models import ChatAnthropic
from langchain.memory import ConversationSummaryBufferMemory
from langchain.tools import BraveSearch
from langchain.prompts.chat import (
    ChatPromptTemplate,
)
from langchain.vectorstores import MongoDBAtlasVectorSearch
from embedder import BertEmbeddings
from medwise import query_medwise
import os

os.environ[
    "ANTHROPIC_API_KEY"] = "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"
CLAUDE_KEY = "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"
BRAVE_API_KEY = "BSAG41ajEpimGNrc59lUGOZ1JbZiB7z"


def get_investigate_prompt(knowledge="", conversation=""):
    template = """The following is a friendly conversation between a doctor and an AI assistant. The AI is talkative and provides lots of specific details from its context. If the AI is not sure of its answer, it says it and explains why it's unsure.
    You will read a consultation between a GP and a patient that has already happened.
     The patient starts by saying their initial story and what they would like help with.
      This is never enough to get to a full diagnosis. In fact the role of an excellent GP is to ask a series of very well phrased questions that most effectively and intelligently dissect the diagnostic search space to reach a set of most probable differential diagnoses, and most importantly to rule out differential diagnoses that are potentially life threatening to the patient, even if they are not the most likely.
    The conversation takes the form of a series of questions (asked by the doctor) and answers (from the patient).

    The full conversation between the doctor and the patient is as follows:
    <conversation>
    {conversation}
    </conversation>
    
    Here is the additional domain knowledge and context that has been retrieved based on the conversation that you should use to make more informed reasoning:
    <knowledge>
    {knowledge}
    </knowledge>
    
    if the {{input}} is "investigate", then your tasks are:

    <tasks>
    As you read through the conversation, pause and think after each important set of responses from the patient. I want you to think of three things given the information you have at each point.
    The top differential diagnoses that explain the symptoms the patient is describing.
    The most dangerous diagnoses that even if unlikely could potentially explain the cluster of symptoms from the patient and that therefore you need to rule out
    And most importantly, given these two types of differentials, what is the most informative next question/set of questions that will allow you to efficiently dissect the diagnostic search space
    At each point, you will internally compare your next best question/set of questions with the clinician’s actual question/set of questions.  

    Finally, as the consultation comes to an end, I want you to work out:
    what are the most likely/dangerous diagnostic spaces/differential diagnoses that the doctor HAS or HAS NOT appropriately enquired about and ruled in or out. (For appropriately I mean that the patient’s answer does not leave scope for misunderstanding, and if it does that it should be clarified.)
    At the end of the consultation, the doctor will give their impression of what is going on, and the next steps they believe should be taken to further clarify what the underlying pathology or pathologies are. At this point, the doctor will ask you “Claude, do you have any further questions or thoughts?” 
    At this point you will suggest the following: 
    What are the most important differential diagnoses that the doctor has not successfully enquired about?  
    What about the consultation makes you believe that?
    What are the most efficient questions, physical exam findings and investigations  to help rule in or out these differentials?

    Make sure that your suggested steps are  structured by history - examination - investigations and that you do not repeat what has already been asked/said by the doctor.

    Also "diagnostic spaces" is a little confusing maybe, just say most probable differential diagnosis including important life-threatening ones that mandate exclusion.
    </tasks>
    
    Else, given your current conversation history with the doctor {{history}}, complete the following task: 
    <task>
    Answer the doctor's question/query. You should use the knowledge and context provided to help you answer the question.
    </task>
    
    AI: Thinking..."""

    template = template.format(knowledge=knowledge, conversation=conversation)

    return PromptTemplate(
        input_variables=["history", "input"], template=template
    )




def get_summary_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful chatbot with a lot of knowledge about the medical domain. You are talking to a patient who is describing their symptoms to you. You want to help them by extracting the most important information."),
        ("human", """I want you to look at the following conversation between a doctor and a patient. 
        
    {conversation}
    
    I want you to now summarize this conversation and extract the key patient symptoms and the key topics and keywords brought up so we can use this to search for relevant domain knowledge.
    Here are 10 textbook chapter titles that you can use as a guide for what to look for:
    
    <chapters>
    "Abdominal pain",
    "Breast lump",
    "Chest pain",
    "Coma and altered consciousness",
    "Confusion: delirium and dementia",
    "Diarrhoea",
    "Dizziness",
    "Dyspepsia",
    "Dyspnoea",
    "Fatigue",
    "Fever",
    "Gasrtointestinal haemorrhage: haematemesis and rectal bleeding",
    "Haematuria",
    "Haemoptysis",
    "Headache",
    "Jaundice",
    "Joint swelling",
    "Leg swelling",
    "Limb weakness",
    "Low back pain",
    "Mobility problems: falls and immobility",
    "Nausea and vomiting",
    "Palpitation",
    "Rash: acute generalized skin eruption",
    "Red eye",
    "Scrotal swelling",
    "Shock",
    "Transient loss of consciousness: syncope and seizures",
    "Urinary incontinence",
    "Vaginal bleeding",
    "Weight loss",
    </chapters>
        
     I want you to tell me what chapters you would like to explore in order to develop a better understanding of the patient's condition. Reply with a structured summary of the conversation and a list of chapters. Each chapter should be enclosed in tags <chapter></chapter>
     
     """),
    ])
    return prompt


def get_keyword_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful chatbot with a lot of knowledge about the medical domain. You are observing a conversation of a patient who is describing their symptoms to a doctor. You want to help them by extracting the most important information from their description. "),
        ("human", """I want you to look at this conversation between a doctor and a patient. I want you to extract three to ten most relevant keywords that summarize the important medical topics related to this patient. Reply with these keywords as a list and nothing else. Each keyword should be enclosed in a <keyword></keyword> tag.
    
    {conversation}
    """),
    ])
    return prompt


class DiagnosisLLM:
    def __init__(self):
        self.keywords = None
        self.summary = None
        self.llm = None
        self.conv_chain = None
        self.summary_chain = None
        self.keyword_chain = None
        self.memory = None
        self.context = None
        self.transcript = None

    def init_conv_chain(self) -> None:
        self.llm = ChatAnthropic(model="claude-2", temperature=0.5)
        self.memory = ConversationSummaryBufferMemory(return_messages=True, llm=self.llm)
        self.get_context()
        knowledge = self.parse_context()
        investigation_prompt = get_investigate_prompt(knowledge, self.transcript)
        self.conv_chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=investigation_prompt,
        )

    def parse_context(self):
        # self.context = {"guidelines": medwise, "textbook": textbook, "web": brave}
        guidelines_knowledge = "<guidelines>\n"
        for item in self.context["guidelines"]:
            text = item["content"]
            guidelines_knowledge += f"<content>\n{text}\n</content>\n\n"
        guidelines_knowledge += "</guidelines>"

        textbook_knowledge = "<textbook>\n"
        for text in self.context["textbook"]:
            textbook_knowledge += f"<content>\n{text}\n</content>\n\n"
        textbook_knowledge += "</textbook>"

        web_knowledge = "<web_search>\n"
        for item in self.context["web"]:
            title = item["title"]
            text = item["snippet"]
            web_knowledge += f"<title>\n{title}\n</title>\n"
            web_knowledge += f"<content>\n{text}\n</content>\n\n"
        web_knowledge += "</web_search>"

        knowledge = guidelines_knowledge + "\n" + textbook_knowledge + "\n" + web_knowledge
        print(knowledge)
        return knowledge

    def new_conv_message(self, message):
        self.conv_chain.run({"input": message})
        print(self.memory)

    def extract_from_transcript(self, transcript):
        self.transcript = transcript
        self.keywords = self.keyword_chain.invoke({"conversation": transcript}).content
        print(self.keywords)
        # Regular expression to find all words enclosed in <keyword> tags
        keywords = re.findall(r'<keyword>(.*?)</keyword>', self.keywords)
        # Join the words into a single string separated by spaces
        self.keywords = ' '.join(keywords)

        time.sleep(2)
        # self.summary = self.summary_chain.invoke({"conversation": transcript}).contents
        print("==========summary========")
        print(self.summary)
        print("==========keywords========")
        print(self.keywords)

    def init_extraction_chains(self) -> None:
        # summary_prompt = get_summary_prompt()
        keyword_prompt = get_keyword_prompt()
        self.llm = ChatAnthropic(model="claude-2", temperature=0.5)
        # self.summary_chain = summary_prompt | self.llm
        self.keyword_chain = keyword_prompt | self.llm

    def get_context_from_brave(self, k=5):
        """
        Uses brave to perform a semantic internet search for relevant medical documents to the provided topics.

        Args:
            topics (list[string]): list of topics for internet search
            k (int, optional): number of documents to return. Defaults to 5.

        Returns:
            _type_: list of k documents
        """

        brave_search_tool = BraveSearch.from_api_key(api_key=BRAVE_API_KEY, search_kwargs={"count": k})
        out = brave_search_tool.run(f"Medical documents on: {self.keywords}")  # TODO prompt engineer improvement
        return out

    def get_context_from_medwise(self, k=1, render_js: bool = False):
        """Performs internet scraping from Medwise for useful documents.

        Args:
            topics (_type_):  list of topics for medwise search
            k (int, optional): number of documents to return. Defaults to 5.

        Returns:
            _type_: ({"url": url, "content": content})
        """

        results = query_medwise(self.keywords, k=k, render_js=render_js)
        return results

    def get_context_from_textbook(self, k=5):
        """
        Performs vector search on mongoDB McLeod clinical diagnosis textbook

        Args:
            summary (string): maximum 512 tokens - the summary of the patient data. Used to query mongoDB
            k (int): number of documents to return

        Returns:
            list[tuple[langchain.schema.document.Document, float]]: [(document, score)]

            Access the document data with document.page_content
        """

        embed = BertEmbeddings(
            model_name="michiyasunaga/BioLinkBERT-large",
            device="cuda" if torch.cuda.is_available() else "cpu",
        )

        MONGODB_ATLAS_CLUSTER_URI = "mongodb+srv://evanrex:c1UgqaM0U2Ay72Es@cluster0.ebrorq5.mongodb.net/?retryWrites=true&w=majority"
        ATLAS_VECTOR_SEARCH_INDEX_NAME = "embedding"

        vector_search = MongoDBAtlasVectorSearch.from_connection_string(
            MONGODB_ATLAS_CLUSTER_URI,
            "macleod_textbook.paragraphs",
            embed,
            index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        )

        results = vector_search.similarity_search_with_score(
            query=self.keywords,
            k=k,
        )  # TODO use paragraph.next and paragraph.prev to get window around returned documents

        results_list = []
        for i, result in enumerate(results):
            doc, score = result
            results_list.append(doc.page_content)
        return results_list

    def get_context(self, k_brave=1, k_medwise=1, k_textbook=1):
        brave = self.get_context_from_brave(k=k_brave)
        print("==============brave=================")
        new_brave = json.loads(brave)
        time.sleep(2)
        medwise = self.get_context_from_medwise(k=k_medwise)
        print("==============medwise=================")
        # print(medwise)
        textbook = self.get_context_from_textbook(k=k_textbook)
        print("==============textbook=================")
        # print(textbook)
        self.context = {"guidelines": medwise, "textbook": textbook, "web": new_brave}
