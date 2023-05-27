import json
import os
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from ..utils import EmbeddingGenerator, cosine_similarity


class DocumentSearch:
    def __init__(self, document_dir: str):
        """
        Initializes the DocumentSearch with a directory containing JSON files.

        Parameters:
        document_dir (str): Directory containing JSON files with document data.
        """
        self.documents_df = self._load_documents(document_dir)
        self.embedding_generator = EmbeddingGenerator()

    def _load_documents(self, document_dir: str) -> pd.DataFrame:
        """
        Loads all documents from JSON files into a DataFrame.

        Parameters:
        document_dir (str): Directory containing JSON files with document data.

        Returns:
        pd.DataFrame: DataFrame containing document data.
        """
        documents = []
        for filename in os.listdir(document_dir):
            if filename.endswith(".json"):
                with open(os.path.join(document_dir, filename)) as f:
                    documents.extend(json.load(f))
        df = pd.DataFrame(documents)
        df["embedding"] = df["embedding"].apply(np.array)
        return df

    def vector_search(self, query: str,
                      data: Optional[pd.DataFrame] = None,
                      top_n: Optional[int] = None) -> pd.DataFrame:
        """
        Performs a vector search with the given query.

        Parameters:
        query (str): The query to search for.
        data (pd.DataFrame, optional): The DataFrame to perform the search on.
                                       If None, self.documents_df is used.
        top_n (int, optional): The number of top documents to return. If None,
                               all documents are returned.

        Returns:
        pd.DataFrame: A DataFrame sorted by similarity to the query, from most to least similar.
        """

        if not data:
            data = self.documents_df

        # for the type checker
        assert data is not None
        
        query_embedding = self.embedding_generator.generate_embeddings([query])[0]
        data["similarity"] = data["embedding"].apply(
            lambda x: cosine_similarity(x, query_embedding)
        )

        # Sort DataFrame by similarity and return top N rows
        sorted_df = data.sort_values(by="similarity", ascending=False)

        # If top_n is specified, return only top_n rows
        if top_n is not None:
            sorted_df = sorted_df.head(top_n)

        return sorted_df

    def filter_metadata(self, filters: Dict[str, str]) -> pd.DataFrame:
        """
        Filters the documents based on the given metadata filters.

        Parameters:
        filters (dict): Dictionary of filters, where each key-value pair represents
                        a column name and a value to filter on.

        Returns:
        pd.DataFrame: DataFrame containing only the rows that meet the filters.
        """
        filtered_df = self.documents_df

        for key, value in filters.items():
            filtered_df = filtered_df[filtered_df[key] == value]

        return filtered_df
