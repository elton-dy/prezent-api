import os
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from my_app_api.models import Message
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory
from decouple import config

os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')

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
    Respond in French.
    Act as an advisor to find the ideal gift. important ask specific voice questions to the user to identify the perfect gift, focusing on understanding the personality of the recipient and give only one gift at a time.
    First, base your suggestions on the conversation history, then on the context.
    Use the following context (enclosed in <ctx></ctx>) and the conversation history (enclosed in <hs></hs>) to respond,
    When a gift is chosen,give the reason and give me juste the id about the product like this ['id' => 'gift id']. doesn't mention product id
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
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.4)
    return llm

def retrieval_qa_chain(llm,db,history):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        return_source_documents=False,
        verbose=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": set_custom_prompt(),
            "memory": get_memory(history)
        }
    )
    return qa_chain

def get_memory(history):

    return ConversationBufferMemory(
            memory_key="history",
            input_key="question",
            chat_memory=history)

def qa_bot(conversation, history):
    db = get_vectorstore()
    llm = load_llm()
    qa = retrieval_qa_chain(llm, db, history)
    return qa

def final_result(query, conversation, db_memory):
    formatted_history = db_memory.get_history()  # Get the conversation history
    # Split the formatted history into individual messages
    history_lines = formatted_history.split('\n')
    print('history: ',history_lines)
    history = ChatMessageHistory()
    # Convert the history lines into tuples or dictionaries
    for line in history_lines:
        speaker, message = line.split(": ", 1)  # Sépare le speaker et le message
        if speaker == 'AI':
            history.add_ai_message(message)
        elif speaker == 'Human':
            history.add_user_message(message)

#     for line in history_lines:
#         if line.startswith("AI: "):
#             # Extrait le message de l'IA en enlevant les 4 premiers caractères ("AI: ")
#             message = line[4:]
#             history.add_ai_message(message)
#         elif line.startswith("Human: "):
#             # Extrait le message de l'utilisateur en enlevant les 7 premiers caractères ("Human: ")
#             message = line[7:]
#             history.add_user_message(message)
    qa_result = qa_bot(conversation, history)  # Pass the history to qa_bot
    response = qa_result.run({"query": query})
    return response

def conversational_chat(query, conversation):
    db_memory = DatabaseMemory(conversation)
    response = final_result(query, conversation, db_memory)
    return response
