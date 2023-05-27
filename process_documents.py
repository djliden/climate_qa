import argparse
from climate_qa import DocumentHandler, IPCC6SummaryForPolicymakersDocument
import os

# import other document types


def main():
    parser = argparse.ArgumentParser(
        description="Process documents for the climate QA system."
    )
    parser.add_argument(
        "--dir", type=str, help="Directory where processed documents should be stored. If not provided, default to ./stored_documents."
    )
    args = parser.parse_args()

    dir_path = args.dir
    if not dir_path:
        dir_path = os.path.join(os.path.dirname(__file__), 'stored_documents')

    # Add the Document objects for all document types you want to process
    documents = [
        IPCC6SummaryForPolicymakersDocument(),
        # other document types...
    ]

    for doc in documents:
        handler = DocumentHandler(document=doc)
        handler.process_document(dir_path=args.dir)


if __name__ == "__main__":
    main()
