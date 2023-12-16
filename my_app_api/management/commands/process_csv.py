import os
from django.core.management.base import BaseCommand
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from decouple import config

class Command(BaseCommand):
    help = 'Process a CSV file to generate a vector database'
    os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')

    def add_arguments(self, parser):
        parser.add_argument('input_path', type=str, help='The path to the CSV file or directory containing CSV files')

    def handle(self, *args, **kwargs):
        input_path = kwargs['input_path']
        persist_directory = 'data/db/news'

        self.process_input_path(input_path, persist_directory)

    def process_csv_file(self, file_path, persist_directory):
        loader = CSVLoader(file_path=file_path, csv_args={"delimiter": ",", "quotechar": '"'})
        documents = loader.load()

        # here we are using OpenAI embeddings but in future we will swap out to local embeddings
        embedding = OpenAIEmbeddings()

        vectordb = Chroma.from_documents(documents=documents, embedding=embedding, persist_directory=persist_directory)
        vectordb.persist()
        self.stdout.write(self.style.SUCCESS(f'Successfully processed {file_path}'))

    def process_input_path(self, input_path, persist_directory):
        if os.path.isdir(input_path):
            for file in os.listdir(input_path):
                if file.endswith(".csv"):
                    file_path = os.path.join(input_path, file)
                    self.process_csv_file(file_path, persist_directory)
        elif os.path.isfile(input_path) and input_path.endswith(".csv"):
            self.process_csv_file(input_path, persist_directory)
        else:
            self.stdout.write(self.style.ERROR('Invalid input path provided. Please provide a valid file or directory path.'))
