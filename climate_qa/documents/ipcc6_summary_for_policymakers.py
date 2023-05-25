"""
This module contains the IPCC6SummaryForPolicymakersDocument class which 
represents the IPCC6 Summary for Policymakers Document.

The document can be read and downloaded from the following url:
https://www.ipcc.ch/report/ar6/wg2/chapter/summary-for-policymakers/
"""

from pypdf import PdfReader
import requests
import re
from .document import Document


class IPCC6SummaryForPolicymakersDocument(Document):
    """
    A class to represent IPCC6 Summary for Policymakers Document.

    This class is a subclass of the abstract class Document and
    provides methods to extract text by section and process it
    from the IPCC6 Summary for Policymakers Document.

    Attributes:
        url (str): URL of the document.
        title (str): Title of the document.
        filename (str): Filename for the downloaded document.
        date (str): Publication date of the document.
        filepath (str): Path where the document is stored locally. Initialized as None.
    """

    url = "https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_SPM.pdf"
    title = "IPCC6 Summary for Policymakers"
    filename = "ipcc6_summary_for_policymakers"
    date = "2023-03-20"

    def __init__(self):
        """
        Constructs all the necessary attributes for the document object.

        Sets the filepath where the document is stored locally to None.
        """
        self.filepath = None

    @staticmethod
    def extract_text_by_section(text):
        """
        Extracts the text by section from the given text.

        Parameters:
            text (str): The text from which to extract.

        Returns:
            list: The list of extracted text by section.
        """
        pattern = r"\b([A-Z]\.\d+\.\d+)\b([\s\S]*?)(?=\b[A-Z]\.\d+\.\d+\b|$)"
        matches = re.findall(pattern, text)
        extracted_text = [match[0] + match[1] for match in matches]
        return extracted_text

    @staticmethod
    def process_extracted_sections(sections):
        """
        Processes the extracted sections by removing figures, boxes, and tables and also
        deleting unwanted text.

        Parameters:
            sections (list): The list of sections to process.

        Returns:
            list: The list of processed sections.
        """
        pattern_fig = r"\[START FIGURE[\s\S]*?END FIGURE\]"
        pattern_box = r"\[START BOX[\s\S]*?END BOX\]"
        pattern_table = r"\[START TABLE[\s\S]*?END TABLE\]"
        extracted_text = [re.sub(pattern_fig, "", t) for t in sections]
        extracted_text = [re.sub(pattern_box, "", t) for t in extracted_text]
        extracted_text = [re.sub(pattern_table, "", t) for t in extracted_text]

        pattern_to_delete = r"\s*\n\s*\n[\s\S]*$"
        extracted_text = [re.sub(pattern_to_delete, "", t) for t in extracted_text]

        i = 0
        while i < len(extracted_text) - 1:
            if re.match(r"^[A-Z]\.\d+\.\d+\)", extracted_text[i + 1]):
                extracted_text[i] += " " + extracted_text[i + 1]
                del extracted_text[i + 1]
            else:
                i += 1

        return extracted_text

    def parse(self):
        """
        Parses the document and extracts and processes the text.

        Returns:
            list: The list of processed sections.
        """
        reader = PdfReader(self.filepath)
        pages = reader.pages
        extracted_pages = []

        for p in reader.pages:
            text = p.extract_text().split("\n")
