from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from myapp.models import Message

class DatabaseMemory:
    def __init__(self, conversation):
        self.conversation = conversation

    def get_history(self):
        messages = Message.objects.filter(conversation=self.conversation).order_by('timestamp')
        history = [(msg.text, msg.message_type) for msg in messages]
        formatted_history = '\n'.join(f'{item[0]}: {item[1]}' for item in history)
        return formatted_history

def get_vectorstore():
    return Chroma(persist_directory="./db/news", embedding_function=OpenAIEmbeddings())

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

def get_chain(conversation):
    return RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=get_vectorstore().as_retriever(search_kwargs={"k":1}),
        return_source_documents=False,
        verbose=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": get_custom_prompt(),
            "memory": DatabaseMemory(conversation)
        }
    )

def conversational_chat(query, conversation):
    memory = DatabaseMemory(conversation)
    formatted_history = memory.get_history()
    response = get_chain(conversation).run({
        "query": query,
        'history': formatted_history
    })
    return response  # Supposons que response contient le texte de réponse de l'IA
