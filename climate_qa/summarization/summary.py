from openai.error import RateLimitError
from ..utils import PromptTemplate, generate_summary
import pandas as pd

class Summarizer:

    summary_prompt = PromptTemplate("""Here is a set of one or more exceprts about a
    topic in climate change:

    <excerpts>
    {excerpts}
    </excerpts>

    Your task is to answer the following question or prompt based on those excerpts:

    <prompt>
    {user_prompt}
    </prompt>

    Begin by very briefly extracting the main point(s) from each excerpt, demarcating this process
    in <thinking> tags. Additionally make note of the source and date of each excerpt,
    and note whether there are any changes across time or disagreements between sources.
    Do not repeat large portions of the text from each excerpt, and do not include new
    <excerpt> tags. The <thinking> section MUST be very short.

    Next, return a short answer to the <prompt> in <response> tags. Here are some rules
    your response must follow:
    - Do not refer to "the excerpts." I.e. say 'according to <report>, ...." not "according
      to the excerpt, ..."
    - If there were any disagreements between sources, note them in the response
    - If there were any changes over time, note them in the response
    - If the excertps mentioned any uncertainties relevant to the prompt/question,
      note them in the response.
    - Recommend the most relevant source as further reading.
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
