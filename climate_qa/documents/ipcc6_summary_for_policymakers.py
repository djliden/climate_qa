from pypdf import PdfReader
import requests
import re

class IPCC6SummaryForPolicymakersDocument:
    url = 'https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_SPM.pdf'
    title = "IPCC6 Summary for Policymakers"
    filename = "ipcc6_summary_for_policymakers"
    date = "2023-03-20"
    
    def __init__(self):
        self.filepath = None

    @staticmethod
    def extract_text_by_section(text):
        pattern = r'\b([A-Z]\.\d+\.\d+)\b([\s\S]*?)(?=\b[A-Z]\.\d+\.\d+\b|$)'
        matches = re.findall(pattern, text)
        extracted_text = [match[0] + match[1] for match in matches]
        return extracted_text

    @staticmethod
    def process_extracted_sections(sections):
        pattern_fig = r'\[START FIGURE[\s\S]*?END FIGURE\]'
        pattern_box = r'\[START BOX[\s\S]*?END BOX\]'
        pattern_table = r'\[START TABLE[\s\S]*?END TABLE\]'
        extracted_text = [re.sub(pattern_fig, '', t) for t in sections]
        extracted_text = [re.sub(pattern_box, '', t) for t in extracted_text]
        extracted_text = [re.sub(pattern_table, '', t) for t in extracted_text]

        pattern_to_delete = r'\s*\n\s*\n[\s\S]*$'
        extracted_text = [re.sub(pattern_to_delete, '', t) for t in extracted_text]

        i = 0
        while i < len(extracted_text) - 1:
            if re.match(r'^[A-Z]\.\d+\.\d+\)', extracted_text[i+1]):
                extracted_text[i] += ' ' + extracted_text[i+1]
                del extracted_text[i+1]
            else:
                i += 1

        return extracted_text

    def parse(self):
        reader = PdfReader(self.filepath)
        pages = reader.pages
        extracted_pages = []
        
        for p in reader.pages:
            text = p.extract_text().split('\n')
            # delete header content
            del text[:3]
            extracted_pages.append('\n'.join(text))
            
        joined_text = '\n'.join(extracted_pages)   
        sections = self.extract_text_by_section(joined_text)
        processed_sections = self.process_extracted_sections(sections)
        
        return processed_sections
