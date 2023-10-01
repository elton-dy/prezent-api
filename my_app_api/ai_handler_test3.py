import os
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from my_app_api.models import Message
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


os.environ["OPENAI_API_KEY"] = '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'

class DatabaseMemory:
    def __init__(self, conversation):
        self.conversation = conversation

    def get_history(self):
        messages = Message.objects.filter(conversation=self.conversation).order_by('timestamp')
        history = [(f"{msg.type}: {msg.text}") for msg in messages]
        formatted_history = '\n'.join(history)
        return formatted_history




def set_custom_prompt():
    custom_prompt_template = """
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
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=["history", "context", "question"])
    return prompt

def get_vectorstore():
    return Chroma(persist_directory="data/db/news", embedding_function=OpenAIEmbeddings())

def load_llm():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    return llm

def retrieval_qa_chain(llm,db,history,conversation):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        return_source_documents=False,
        verbose=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": set_custom_prompt(),
            "memory": get_memory(conversation)
        }
    )
    return qa_chain

def get_memory(conversation):
    db_memory = DatabaseMemory(conversation)
    return ConversationBufferMemory(
            memory_key="history",
            input_key="question",
            chat_memory=db_memory.get_history())

def qa_bot(conversation, history):
    db = get_vectorstore()
    llm = load_llm()
    qa = retrieval_qa_chain(llm, db, history,conversation)
    return qa

def final_result(query, conversation, db_memory):
    formatted_history = db_memory.get_history()  # Get the conversation history
    # Split the formatted history into individual messages
    history_lines = formatted_history.split('\n')
    # Convert the history lines into tuples or dictionaries
    history = [('bonjour', "Bonjour! Comment puis-je vous aider aujourd'hui?"), ('je cherche un cadeau', 'Bien sûr! Je serais ravi de vous aider à trouver le cadeau parfait. Pour commencer, pour qui recherchez-vous ce cadeau?')]
#     for line in history_lines:
#         speaker, message = line.split(': ', 1)
#         history.append((speaker, message))

    print('question')
    print(query)

    qa_result = qa_bot(conversation, history)  # Pass the history to qa_bot
    response = qa_result.run({"query": query})
    return response

def conversational_chat(query, conversation):
    db_memory = DatabaseMemory(conversation)
    response = final_result(query, conversation, db_memory)
    return response
