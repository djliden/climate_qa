from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import openai
import os
import re
from dotenv import load_dotenv
load_dotenv()


class EmbeddingGenerator:
    def __init__(self, model_name: str = "msmarco-distilroberta-base-v2"):
        """
        Initializes the EmbeddingGenerator with a SentenceTransformer model.

        Parameters:
        model_name (str): Name of the model to use for generating embeddings.
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, text: List[str]) -> np.ndarray:
        """
        Generates embeddings for the given text.

        Parameters:
        text (List[str]): List of strings to generate embeddings for.

        Returns:
        np.ndarray: The embeddings generated by the model.
        """
        return self.model.encode(text)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """computes the cosine similarity between vectors a and b"""
    return np.dot(a, b) / (norm(a) * norm(b))


def generate_summary(
    prompt: str, stream: bool = False, model: str = "gpt-3.5-turbo"
) -> str:
    """
    Generates text using the OpenAI GPT model.

    Parameters:
    prompt (str): The input prompt for the model.
    stream (bool, optional): Whether to use streaming for the output.
                             If True, prints output incrementally as it becomes available.
    model (str, optional): The GPT model to use. Default is "gpt-3.5-turbo".

    Returns:
    str: The generated text.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not stream:
        completion = openai.ChatCompletion.create(
            model=model, messages=[{"role": "system", "content": prompt}]
        )
        return completion.choices[0].message.content
    else:
        result = []
        response = openai.ChatCompletion.create(
            model=model, messages=[{"role": "system", "content": prompt}], stream=True
        )
        for r in response:
            out = r.choices[0]["delta"]
            answer = out.get("content", "")
            result.append(answer)
            print(answer, end="", flush=True)
        result = "".join(result)
        return result


class PromptTemplate:
    """
    A class that holds a template string with placeholders and allows generating
    specific queries using keyword arguments.
    """

    def __init__(self, template):
        """
        Initialize the PromptTemplate with the given template string.

        Args:
            template (str): A template string with placeholders enclosed in
                            curly braces, e.g. "{user_input} and {schema}"
        """
        self.template = template
        self.arguments = re.findall(r"{(\w+)}", template)


    def format_prompt(self, **kwargs):
        """
        Populate the template string with the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments corresponding to placeholders in the template.

        Returns:
            str: The populated template string.
        """
        return self.template.format(**kwargs)
    
    def __call__(self, **kwargs):
        """
        Make the PromptTemplate object callable.

        Args:
            **kwargs: Keyword arguments corresponding to placeholders in the template.

        Returns:
            str: The populated template string.
        """
        return self.format_prompt(**kwargs)
    
    def __repr__(self):
        """
        Returns a string representation of the object, including the template
        string and the expected arguments.

        Returns:
            str: String representation of the PromptTemplate object.
        """
        return f"PromptTemplate(template='{self.template}'\nexpected_arguments={self.arguments})"
