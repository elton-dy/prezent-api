import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from my_app_api.models import Message
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = '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'

class DatabaseMemory:
    def __init__(self, conversation):
        self.conversation = conversation

    def get_history(self):
        messages = Message.objects.filter(conversation=self.conversation).order_by('timestamp')
        history = [(f"{msg.type}: {msg.text}") for msg in messages]
        formatted_history = '\n'.join(history)
        return formatted_history

def get_vectorstore():
    return Chroma(persist_directory="data/db/news", embedding_function=OpenAIEmbeddings())

def get_custom_prompt():
    template = """
    Répondez en français.
    comporte toi comme un conseille qui aide a trouver le cadeau parfait, pose des question a l'utilisateur pour savoir quel cadeau proposer.
    Utilisez d'abord l'historique de la conversation, puis le contexte.
    Utilisez le contexte suivant (délimité par <ctx></ctx>) et l'historique de la conversation (délimité par <hs></hs>) pour répondre à la question :
    ------
    <ctx>
    {context}
    </ctx>
    ------
    <hs>
    {history}
    </hs>
    ------
    {question}
    Réponse :"""

    return PromptTemplate(
        input_variables=["history", "context", "question"],
        template=template,
    )

def get_llm():
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def get_memory(conversation):
    db_memory = DatabaseMemory(conversation)
    return ConversationBufferMemory(
            human_prefix='User',
            ).add_memory(db_memory.get_history())
def get_chain(conversation):
    db_memory = DatabaseMemory(conversation)
    # Convertir l'objet DatabaseMemory en un dictionnaire
    memory_dict = {
        "history": db_memory.get_history(),
    }

    return RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=get_vectorstore().as_retriever(search_kwargs={"k":1}),
        return_source_documents=False,
        verbose=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": get_custom_prompt(),
            "memory": get_memory(conversation)
        }
    )

def conversational_chat(query, conversation):
    memory = DatabaseMemory(conversation)
    formatted_history = memory.get_history()
    print('ici')
    response = get_chain(conversation).run({
        "query": query,
        'history': formatted_history
    })
    print(response)
    exit()
    return response  # Supposons que response contient le texte de réponse de l'IA
