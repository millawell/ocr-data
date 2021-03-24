from pathlib import Path
import pandas as pd
from lxml import etree


def parse_mets(pdf_name):
    path_to_mets = Path("../data/mets/pdf_name").with_suffix("mets")
    import pdb; pdb.set_trace()


def get_pdf_pages_of_book(pdf_name):
    sheet = parse_mets(pdf_name)
    try:
        return sheet[sheet.pdf_renamed == pdf_name].iloc[0].pdf_pages
    except IndexError:
        raise ValueError(f"Pdf name {pdf_name} not found in sheet.")
