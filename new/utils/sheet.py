import pandas as pd

def parse_sheet(path):
    sheet = pd.read_csv(path, sep="\t")
    sheet = pd.DataFrame(sheet[sheet.pdf_pages != 'unused'])
    sheet['pdf_pages'] = sheet[sheet.pdf_pages != 'unused'].pdf_pages.apply(eval)
    sheet['printed_page_number'] = sheet[sheet.printed_page_number != 'unused'].printed_page_number.apply(eval)
    return sheet


def get_pdf_pages_of_book(pdf_name):
    sheet = parse_sheet('../data/sheet/corpus-scott-shakespeare-translations.tsv')
    try:
        return sheet[sheet.pdf_renamed == pdf_name].iloc[0].pdf_pages
    except IndexError:
        raise ValueError(f"Pdf name {pdf_name} not found in sheet.")
    

def get_sheet_record(pdf_name):
    sheet = parse_sheet('../data/sheet/corpus-scott-shakespeare-translations.tsv')
    try:
        return sheet[sheet.pdf_renamed == pdf_name].iloc[0]
    except IndexError:
        raise ValueError(f"Pdf name {pdf_name} not found in sheet.")
    
