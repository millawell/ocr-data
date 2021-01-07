


def main(pdf_path):

    pdf_file_name = Path(pdf_path).name

    sheet_record = get_sheet_record(pdf_file_name)

    images = extract_images(pdf_path)