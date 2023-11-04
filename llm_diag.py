import datetime

from langchain.prompts import PromptTemplate
from loguru import logger
import os
import time
from langchain.chains import create_extraction_chain
import torch
from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st
from langchain.callbacks import FileCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.tools import BraveSearch
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents import Tool

from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import Chroma

from langchain.vectorstores import MongoDBAtlasVectorSearch
from embedder import BertEmbeddings

from medwise import query_medwise

import os

os.environ[
    "ANTHROPIC_API_KEY"] = "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"

# import constants
# from constants import *

CLAUDE_KEY = "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"
BRAVE_API_KEY = "BSAG41ajEpimGNrc59lUGOZ1JbZiB7z"

logfile = "output.log"

logger.add(logfile, colorize=True, enqueue=True)
handler = FileCallbackHandler(logfile)


# def load_confluence_spaces():
#     spaces = CONFLUENCE.get_all_spaces(start=0, limit=500, expand="homepage")['results']
#     return [space['key'] for space in spaces]
#
#
# def load_confluence_documents(space_key):
#     return CONFLUENCE_LOADER.load(space_key=space_key, limit=100, content_format=ContentFormat.VIEW)
#
#
# def load_confluence_documents_from_page_ids(page_ids):
#     return CONFLUENCE_LOADER.load(page_ids=page_ids)


def get_text_from_docs(docs):
    return [doc.page_content for doc in docs]


def get_investigate_prompt():
    custom_prompt = """You are a Confluence chatbot answering questions. USe the following pieces of context to answer the question at the end.
            If you don't know the answer, say that you don't know, don't try to make up an answer.  
            Human: {human_message}
            {context}

            Question: {question}
            Helpful Answer:"""

    return ChatPromptTemplate(
        template=custom_prompt,
        human_prompt_name="Doctor",
        human_message_key="human_message",
    )


def get_extraction_prompt():
    custom_prompt = """You are a Confluence chatbot answering questions. USe the following pieces of context to answer the question at the end.
            If you don't know the answer, say that you don't know, don't try to make up an answer.  
            Human: {human_message}
            {context}

            Question: {question}
            Helpful Answer:"""
    return PromptTemplate(
        template=custom_prompt, input_variables=["conversation"]
    )


def get_quick_answer():
    chat = ChatAnthropic(model='claude-2')
    messages = [
        HumanMessage(
            content="Can you please summarize this conversation in "
        )
    ]
    chat(messages)


class DiagnosisLLM:
    def __init__(self):
        self.embedding = None
        self.vectordb = None
        self.llm = None
        self.conv_chain = None
        self.extraction_chain = None
        self.retriever = None
        self.memory = None
        self.docs = None
        self.embeddings_map = {}

    # TODO: Use the BERT biomedicine embeddings instead
    def init_embeddings(self) -> None:
        pass

    def init_conv_chain(self) -> None:
        self.llm = ChatAnthropic(model="claude-2", temperature=0.5)
        memory = ConversationSummaryBufferMemory(memory_key="chat_history", return_messages=True)
        self.retriever = None
        self.conv_chain = ConversationalRetrievalChain(
            llm=self.llm,
            memory=memory,
            retriever=self.retriever,
        )

    def init_extraction_chain(self) -> None:
        schema = {
            "properties": {
                "patient_symptoms": {"type": "string"},
                "conversation_summary": {"type": "string"},
                "conversation_keywords": {"type": "string"},
                "patient_extra_info": {"type": "string"},
            },
        }
        self.extraction_chain = create_extraction_chain(schema, self.llm, prompt=get_extraction_prompt())

    def extract_from_transcript(self, transcript):
        return self.extraction_chain.run(transcript)

    # def web_search(self, query):
    #     return brave_search_tool.run(query)

    def get_context_from_brave(self, topics, k=5):
        """
        Uses brave to perform a semantic internet search for relevant medical documents to the provided topics.

        Args:
            topics (list[string]): list of topics for internet search
            k (int, optional): number of documents to return. Defaults to 5.

        Returns:
            _type_: list of k documents
        """

        brave_search_tool = BraveSearch.from_api_key(api_key=BRAVE_API_KEY, search_kwargs={"count": k})
        print(brave_search_tool)
        out = brave_search_tool.run(f"Medical documents on: {topics}") # TODO prompt engineer improvement
        return out
        # tools = [
        #     Tool(
        #         name="Current Search",
        #         func=brave_search_tool.run,
        #         description="useful for when you need to answer questions about current events or the current state of the world"
        #     ),
        # ]
        # self.memory = ConversationSummaryBufferMemory(memory_key="chat_history", return_messages=True, llm=self.llm)
        #
        # agent_chain = initialize_agent(tools,
        #                                self.llm,
        #                                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        #                                verbose=True,
        #                                memory=self.memory)
        # agent_chain.run(input=question)

    def get_context_from_medwise(self, topics, k=5, render_js: bool = False):
        """Performs internet scraping from Medwise for useful documents.

        Args:
            topics (_type_):  list of topics for medwise search
            k (int, optional): number of documents to return. Defaults to 5.

        Returns:
            _type_: ({"url": url, "content": content})
        """

        query = " ".join(topics)

        results = query_medwise(query, k=k, render_js=render_js)
        return results

    def get_context_from_textbook(self, summary, k=5):
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
            query=summary,
            k=k,
        ) # TODO use paragraph.next and paragraph.prev to get window around returned documents


        # Display results
        # for i, result in enumerate(results):
        #     content, score = result
        #     print(i, score)
        #     print(content.page_content)
        return results

    def load_confluence_documents_from_all_spaces(self):
        if self.docs is not None:
            return self.docs
        # space_keys = load_confluence_spaces()
        target_spaces = ['INF', 'RD']
        all_docs = []
        for space_key in target_spaces:
            logger.info(f"Loading documents from space with key {space_key}")
            confluence_docs = load_confluence_documents(space_key)
            all_docs.extend(confluence_docs)
        self.docs = all_docs
        logger.info(f"Loaded {len(self.docs)} documents from {constants.confluence_domain}")
        return all_docs

    def extract_all_recently_modified_docs(self):
        all_docs = self.load_confluence_documents_from_all_spaces()
        page_ids = [doc.metadata["id"] for doc in all_docs]
        last_updated_dates = {}
        for page_id in page_ids:
            history = CONFLUENCE.history(page_id)
            last_updated_dates[page_id] = (
                datetime.datetime.strptime(history["lastUpdated"]["when"][0:10], "%Y-%m-%d").strftime("%Y-%m-%d"))
        sorted_last_updated = dict(sorted(last_updated_dates.items(), key=lambda x: x[1], reverse=True))
        date = list(sorted_last_updated.items())[0][1]
        docs_to_update = list({k: v for k, v in sorted_last_updated.items() if v == date}.keys())
        return docs_to_update

    def vector_db_confluence_docs(self, force_reload: bool = False) -> None:
        """
        creates vector db for the embeddings and persists them or loads a vector db from the persist directory
        """
        if persist_directory and os.path.exists(persist_directory) and not force_reload:
            ## Load from the persist db
            logger.info("Loading vector database")
            self.vectordb = Chroma(persist_directory=persist_directory, embedding_function=self.embedding,
                                   collection_name="Torstone")
            logger.info(f"Vector embedding database successfully loaded from {persist_directory}")

        else:
            logger.info("Loading Confluence documents")
            ## 1. Extract the documents
            documents = self.load_confluence_documents_from_all_spaces()
            logger.info("Splitting texts")
            ## 2. Split the texts
            # Use only the TokenTextSplitter to ensure token boundaries are respected
            text_splitter = TokenTextSplitter(chunk_size=3000, chunk_overlap=50,
                                              encoding_name="cl100k_base")  # Increase chunk_overlap if needed
            split_documents = text_splitter.split_documents(documents)

            texts = [doc.page_content for doc in split_documents]
            client = chromadb.PersistentClient(path=persist_directory)
            self.vectordb = Chroma(client=client, persist_directory=persist_directory,
                                   embedding_function=self.embedding, collection_name="Torstone")
            delay_factor = 1.0
            ## 3. Create Embeddings and add to chroma store
            while True:
                try:
                    # embeddings = self.get_embeddings(texts)
                    ids = [str(e) for e in list(range(0, len(texts)))]
                    metadatas = [doc.metadata for doc in split_documents]
                    logger.info(
                        f"Creating embeddings for {len(split_documents)} documents and storing in vector database")
                    embeddings = self.get_embeddings(texts)
                    self.vectordb._collection.add(ids=ids, metadatas=metadatas, embeddings=embeddings, documents=texts)
                    logger.info(f"Vector embedding database successfully created and stored in {persist_directory}")

                except Exception as e:
                    logger.error(f"API Error: {e}")
                    logger.debug(f"Retrying in 10 seconds...")
                    time.sleep(10 * delay_factor)
                    delay_factor += 0.1
                    continue
                break

    # TODO: Get embeddings from BERT instead (the biomedicine one)
    def get_embeddings(self, documents):
        pass
        embeddings = []
        index = 0
        for doc in documents:
            response = openai.Embedding.create(model="text-embedding-ada-002", input=[doc],
                                               openai_api_key=OPEN_AI_API_KEY)
            embeddings.append(response['data'][0]['embedding'])
            index += 1
            time.sleep(0.2)
        return embeddings

    def retrieval_qa_chain(self):
        """
        Creates retrieval qa chain using vectordb as retriever and LLM to complete the prompt
        """
        custom_prompt = """You are a Confluence chatbot answering questions. USe the following pieces of context to answer the question at the end.
        If you don't know the answer, say that you don't know, don't try to make up an answer.  

        {context}

        Question: {question}
        Helpful Answer:"""
        custom_prompt_template = PromptTemplate(
            template=custom_prompt, input_variables=["context", "question"]
        )
        ## Inject custom prompt
        self.memory = ConversationSummaryBufferMemory(memory_key="chat_history", return_messages=True, llm=self.llm,
                                                      output_key="answer")

        # TODO: Use MongoDB here instead
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": 5})
        self.qa_chain = ConversationalRetrievalChain.from_llm(llm=self.llm,
                                                              retriever=self.retriever,
                                                              combine_docs_chain_kwargs={
                                                                  "prompt": custom_prompt_template},
                                                              return_source_documents=True,
                                                              memory=self.memory,
                                                              )

    def get_chat_history(self, output, sources):
        chat_history = []
        for message in output["chat_history"]:
            role = message.type.upper()
            chat_history.append({"role": role, "content": message.content})
        # chat_history[-1]["content"] += "\n"
        # chat_history[-1]["content"] += sources
        return chat_history

    def answer_confluence(self, question: str):
        """
        Answer the question
        """
        result = self.qa_chain({"question": question})
        retrieved_documents = result['source_documents']
        total_length = sum([len(doc.page_content) for doc in retrieved_documents])
        print(total_length)
        print(self.qa_chain.combine_docs_chain.llm_chain.prompt)
        search = self.vectordb.similarity_search_with_score(question, k=5)
        print(search)
        links = [doc.metadata['source'] for doc in retrieved_documents]
        sources = "\n ".join(links)
        chat_history_so_far = self.get_chat_history(result, sources)
        answer = result['answer']
        logger.info(f"Question asked: {question}")
        logger.info(f"Documents in which information was found: \n {sources}")
        logger.info(f"Chat history: \n {chat_history_so_far}")
        logger.info(f"Answer to the question:\n {answer}")
        return {"answer": answer, "chat_history": chat_history_so_far, "sources": links}

    def display_documents(self, question):
        search = self.vectordb.similarity_search_with_score(question, k=5)
        try:
            st.write("This information was found in:")
            for doc in search:
                score = doc[1]
                try:
                    page_num = doc[0].metadata['page']
                except:
                    page_num = "txt snippets"
                source = doc[0].metadata['source']
                # With a streamlit expander
                with st.expander(
                        "Source: " + str(source) + " - Page: " + str(page_num) + "; Similarity Score: " + str(score)):
                    st.write(doc[0].page_content)
        except Exception as e:
            logger.error(e)
            logger.error("unable to get source document detail")

    # def update_docs(self):
    #     collection = self.vectordb._client.get_collection("ConfluenceDocs")
    #     collection_content = collection.get()
    #     metadatas = collection_content['metadatas']
    #     embedding_ids = collection_content['ids']
    #     self.embeddings_map = {metadatas[i]['id']: embedding_ids[i] for i in range(len(metadatas))}
    #     page_ids = self.extract_all_recently_modified_docs()
    #     documents = load_confluence_documents_from_page_ids(page_ids)
    #     texts = get_text_from_docs(documents)
    #     embedding_ids_to_update = [self.embeddings_map[page_id] for page_id in page_ids]
    #     self.vectordb.add_texts(texts=texts, ids=embedding_ids_to_update)
