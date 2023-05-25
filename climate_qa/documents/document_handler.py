"""
document_handler.py

This module contains the DocumentHandler class which is responsible for managing
the lifecycle of a document. The DocumentHandler utilizes strategy pattern to
allow for different handling of different document types.
"""
#import sys
#sys.path.append("../")
from re import error
import requests
import tempfile
import os
from sentence_transformers import SentenceTransformer
import json
from typing import Union
from .document import Document
from ..utils import EmbeddingGenerator


class DocumentHandler:
    """
    DocumentHandler class

    This class is responsible for handling the lifecycle of a document. It uses
    strategy pattern to delegate the actual processing (download, extract text,
    generate embeddings) to the document object that's passed to it during
    instantiation.
    """

    def __init__(self, document: Document):
        """
        Initializes the DocumentHandler with a specific document object.

        Parameters:
        document (object): An instance of a Document class (like IPCCDocument,
                           UNFCCCDocument, etc.) which defines how to download
                           and extract text from a specific type of document.
        """
        self.document = document
        self.embedding_generator = EmbeddingGenerator()

    def download(self) -> None:
        """
        Download the document from the url specified in the document object
        """
        url = self.document.url
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
            tf.write(response.content)
            # sets document.filepath
            self.document.filepath = tf.name
            

    def extract_text(self) -> None:
        """
        Extract text from the document using the method defined in the document
        object. Returns a list of sections from which we can then generate
        vector embeddings.
        """
        try:
            self.processed_sections = self.document.parse()
        finally:
            os.remove(self.document.filepath)

    def generate_embeddings(self) -> None:
        """
        Generate embeddings for the document text.
        """
        self.embeddings = self.embedding_generator.generate_embeddings(self.processed_sections)

    def store_document(self, dir_path: Union[str, None] = None) -> None:
        """
        Store the document sections, embeddings, and metadata as a
        JSON file.

        Parameters:
        dir_path (str): directory where the JSON file should be saved.
                        default to project root directory.
        """

        data = []
        for i in range(len(self.processed_sections)):
            d = {
                "title": self.document.title,
                "date": self.document.date,
                "url": self.document.url,
                "text": self.processed_sections[i],
                "embedding": self.embeddings[i].tolist(),
                "embedding_model": self.embedding_generator.model_name
            }
            data.append(d)

        # save documents
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        if dir_path is None:
            dir_path = project_root

        stored_documents_path = os.path.join(dir_path, "stored_documents")

        # Check if the directory exists, if not create one
        if not os.path.exists(stored_documents_path):
            os.makedirs(stored_documents_path)

        # Define the filename. Here we are using the title of the document.
        # In real scenario, you might want to use unique identifiers.
        file_name = f"{self.document.filename}.json"
        file_path = os.path.join(stored_documents_path, file_name)

        # Write the data to a json file
        with open(file_path, "w") as f:
            json.dump(data, f)
