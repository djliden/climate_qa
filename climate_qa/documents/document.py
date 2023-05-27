from abc import ABC, abstractmethod
from typing import List


class Document(ABC):
    """
    Abstract base class for document types.

    Subclasses are expected to define class-level properties:
    - url: str
    - title: str
    - filename: str
    - date: str

    And implement methods:
    - extract_text_by_section(self, text): Process the extracted text by sections.
    - process_extracted_sections(self, sections): Further process the extracted sections.
    - parse(self): Parse the document to extract and process the text.
    """

    url: str
    title: str
    filename: str
    date: str

    @abstractmethod
    def parse(self) -> List[str]:
        """
        Parse the document.

        Returns:
        List[str]: List of parsed sections of the document.
        """
        pass
