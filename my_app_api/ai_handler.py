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
        return Message.objects.filter(conversation=self.conversation).order_by('timestamp')

def set_custom_prompt():
    custom_prompt_template = """
    Respond in French.
    Act as an advisor to find the ideal gift. important ask specific voice questions to the user to identify the perfect gift, focusing on understanding the personality of the recipient and give only one gift at a time.
    First, base your suggestions on the conversation history, then on the context.
    Use the following context (enclosed in <ctx></ctx>) and the conversation history (enclosed in <hs></hs>) to respond,
    Important when a gift is chosen,give the reason and give me juste the id about the product like this ['id' => 'the gift id']. doesn't mention product id.
    if you can't find a gift, juste says so
    example of answer: she gift that could correspond to you would be a headphone for listening to music  ['id' => '15']
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
    llm = ChatOpenAI(model_name="gpt-4-0613", temperature=0.6)
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
    messages = db_memory.get_history()  # Get the conversation history
    history = ChatMessageHistory()

    for message in messages:
        if message.type == 'AI':
            history.add_ai_message(message.text)
        elif message.type == 'Human':
            history.add_user_message(message.text)
    qa_result = qa_bot(conversation, history)  # Pass the history to qa_bot
    response = qa_result.run({"query": query})
    return response

def conversational_chat(query, conversation):
    db_memory = DatabaseMemory(conversation)
    response = final_result(query, conversation, db_memory)
    return response
