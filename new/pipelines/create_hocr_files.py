import sys
sys.path.append("../utils/")
import numpy as np
from pathlib import Path
from sheet import get_sheet_record, get_pdf_pages_of_book
from transcriptions import get_bounding_boxes_from_transcription
from pdfs import extract_images
from jinja2 import Environment, FileSystemLoader
from kraken.serialization import _rescale


def serialize(records, urlpdf):
    pages = []
    for rec in records:
        image_name = rec["image_name"]
        image_size = rec["image_size"]
        writing_mode = rec["writing_mode"]
        lines = rec["lines"]

        page = {'lines': [], 'size': image_size, 'name': image_name, 'writing_mode': writing_mode, 'scripts': None}  # type: dict
        seg_idx = 0
        char_idx = 0
        for idx, record in enumerate(lines):
            line = {'index': idx,
                    'bbox': record["bbox"],
                    'text': record["text"]
                    }
            page['lines'].append(line)
        pages.append(page)

    env = Environment(
        loader=FileSystemLoader('../templates'),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True
    )
    env.tests['whitespace'] = str.isspace
    env.filters['rescale'] = _rescale
    tmpl = env.get_template("hocr_lines.xml")
    return tmpl.render(pages=pages, urlpdf=urlpdf)


def main(pdf_path):

    pdf_file_name = Path(pdf_path).name

    sheet_record = get_sheet_record(pdf_file_name)
    pages = get_pdf_pages_of_book(pdf_file_name)
    images = extract_images(pdf_path)
    our_identifiers = sheet_record.identifier
    if isinstance(our_identifiers, str):
        our_identifiers = [our_identifiers]

    transcribes = []
    for our_identifier in our_identifiers:
        transcribe_dir = Path(f"../data/transcriptions/{our_identifier}/")
        transcribes += [p for p in transcribe_dir.iterdir() if p.name.startswith('transcribe')]
    
    bboxes = []
    for transcribe in transcribes:
        bboxes += get_bounding_boxes_from_transcription(str(transcribe))

    render_set = []
    for page_nr, (_, image), rec in zip(pages, images, bboxes):
        render_set.append({
            "image_name": page_nr,
            "image_size": np.asarray(image).shape,
            "writing_mode": rec["writing_mode"],
            "lines": rec["lines"]
        })

    serialized = serialize(render_set, sheet_record.book_url)
    
    output_path = Path(f"../data/xml_output/{pdf_file_name}")
    output_path = output_path.with_suffix(".hocr")
    with open(output_path, "w") as fout:
        fout.write(serialized)

main('../data/pdf_renamed/1VUJAAAAQAAJ.pdf')