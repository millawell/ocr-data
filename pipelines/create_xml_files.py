import sys
sys.path.append("../utils/")
import click
import numpy as np
from pathlib import Path
from sheet import get_sheet_record, get_pdf_pages_of_book
from transcriptions import get_bounding_boxes_from_transcription
from pdfs import extract_images
from jinja2 import Environment, FileSystemLoader
from kraken.serialization import _rescale


def serialize(records, urlpdf, langauge):
    pages = []
    for rec in records:
        image_name = rec["image_name"]
        
        writing_mode = rec["writing_mode"]
        lines = rec["lines"]

        page = {
            'lines': [], 
            'image_height': rec["image_height"], 
            'image_width': rec["image_width"], 
            'name': image_name, 
            'writing_mode': writing_mode, 
            'scripts': None, 
            'text': rec['text']
        }  # type: dict

        seg_idx = 0
        char_idx = 0
        for idx, record in enumerate(lines):

            line = {'index': idx,
                    'top_left': f"{record['bbox'][1]},{record['bbox'][0]}",
                    'top_right': f"{record['bbox'][1]},{record['bbox'][2]}",
                    'bottom_right': f"{record['bbox'][3]},{record['bbox'][2]}",
                    'bottom_left': f"{record['bbox'][3]},{record['bbox'][0]}",
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
    tmpl = env.get_template("page.xml")
    return tmpl.render(pages=pages, urlpdf=urlpdf, language=langauge)

@click.command()
@click.option('--pdf_path')
def main(pdf_path):

    pdf_file_name = Path(pdf_path).name
    identifier = Path(pdf_path).stem

    sheet_record = get_sheet_record(pdf_file_name)
    pages = get_pdf_pages_of_book(pdf_file_name)
    images = extract_images(pdf_path)

    transcribe_dir = Path(f"../data/transcriptions/{identifier}/")
    transcribes = [p for p in transcribe_dir.iterdir() if p.name.startswith('transcribe')]
    transcribes = sorted(transcribes)

    bboxes = []
    for transcribe in transcribes:
        bboxes += get_bounding_boxes_from_transcription(str(transcribe))

    render_set = []
    for page_nr, (_, image), rec in zip(pages, images, bboxes):

        render_set.append({
            "image_name": page_nr,
            "image_width": rec["image_size"][0],
            "image_height": rec["image_size"][1],
            "writing_mode": rec["writing_mode"],
            "lines": rec["lines"],
            "text": "\n".join([l['text'] for l in rec["lines"]])
        })

    serialized = serialize(
        render_set,
        sheet_record.book_url,
        sheet_record.language
    )
    
    output_path = Path(f"../data/xml_output/{pdf_file_name}")
    output_path = output_path.with_suffix(".xml")
    with open(output_path, "w") as fout:
        fout.write(serialized)

if __name__ == '__main__':
    main()