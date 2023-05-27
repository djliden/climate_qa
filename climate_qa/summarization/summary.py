import pandas as pd
from openai.error import RateLimitError

from ..utils import PromptTemplate, generate_summary


class Summarizer:

    summary_prompt = PromptTemplate("""
    <excerpts>
    {excerpts}
    </excerpts>

    Based on these documents, please:

    1. Briefly extract the main points in <thinking> tags. Note sources, dates, changes over time, and disagreements. Keep this very short and do not repeat large text portions.

    2. Answer the following question in <response> tags:
    {user_prompt}

    Rules for the response:
    - Refer directly to the source, not as 'the excerpts.'
    - Highlight any disagreements or changes over time.
    - Mention relevant uncertainties.
    - Recommend the most relevant source for further reading.
    """)
    
    def __init__(self, excerpts: pd.DataFrame):
        self.excerpts = excerpts
        self.processed_excerpts = self._preprocess_excerpts()

    def _preprocess_excerpts(self) -> str:
        """processes document excerpts into a string representation with
        metadata"""

        processed_excerpts_list = []

        for _,r in self.excerpts.iterrows():
            processed_excerpts_list.append(f"""document: {r.title}
date: {r.date}
text: {r.text}
================================================================================
""")
        return '\n'.join(processed_excerpts_list)
    

    def summarize(self, prompt, stream:bool = False) -> str:
        prompt = self.summary_prompt(excerpts = self.processed_excerpts, user_prompt = prompt)
        try:
            return generate_summary(prompt, stream=stream)
        except RateLimitError as e:
            print("Rate limit exceeded. Please try again.")
            return ""
