import os
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from my_app_api.models import Message
from langchain.embeddings import OpenAIEmbeddings


os.environ["OPENAI_API_KEY"] = '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'

class DatabaseMemory:
    def __init__(self, conversation):
        self.conversation = conversation

    def get_history(self):
        messages = Message.objects.filter(conversation=self.conversation).order_by('timestamp')
        history = [(f"{msg.type}: {msg.text}") for msg in messages]
        formatted_history = '\n'.join(history)
        return formatted_history

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

------
{question}
Réponse :
"""

def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

def get_vectorstore():
    return Chroma(persist_directory="data/db/news", embedding_function=OpenAIEmbeddings())

def load_llm():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    return llm

def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=db.as_retriever(search_kwargs={'k': 1}),
                                           return_source_documents=False,
                                           chain_type_kwargs={'prompt': prompt}
                                           )
    return qa_chain

def qa_bot(conversation):
    db = get_vectorstore()
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa

def final_result(query, conversation, db_memory):
    qa_result = qa_bot(conversation)
    response = qa_result.run({'query': query, 'context': ''})
    return response

def conversational_chat(query, conversation):
    db_memory = DatabaseMemory(conversation)
    response = final_result(query, conversation, db_memory)
    print('ICI:')
    print(response)
    print('ICI:')
    return response  # Suppose que response contient le texte de réponse de l'IA
