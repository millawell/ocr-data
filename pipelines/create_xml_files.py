import sys
sys.path.append("../utils/")
import click
import numpy as np
from pathlib import Path
from mets import parse_mets, get_pdf_pages_of_book
from transcriptions import get_bounding_boxes_from_transcription
from pdfs import extract_images
from jinja2 import Environment, FileSystemLoader
from kraken.serialization import _rescale

def serialize_page(rec, urlpdf, langauge):
    
    page = {
        'lines': [], 
        'image_height': rec["image_height"], 
        'image_width': rec["image_width"], 
        'name': rec["image_name"], 
        'writing_mode': rec["writing_mode"], 
        'scripts': None, 
        'text': rec['text']
    } 
    for idx, record in enumerate(rec["lines"]):

        line = {'index': idx,
                'top_left': f"{record['bbox'][1]},{record['bbox'][0]}",
                'top_right': f"{record['bbox'][1]},{record['bbox'][2]}",
                'bottom_right': f"{record['bbox'][3]},{record['bbox'][2]}",
                'bottom_left': f"{record['bbox'][3]},{record['bbox'][0]}",
                'text': record["text"]
                }
        page['lines'].append(line)
    
    env = Environment(
        loader=FileSystemLoader('../templates'),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True
    )
    env.tests['whitespace'] = str.isspace
    env.filters['rescale'] = _rescale
    tmpl = env.get_template("page.xml")
    return tmpl.render(page=page, urlpdf=urlpdf, language=langauge)


@click.command()
@click.option('--pdf_path')
def main(pdf_path):

    pdf_file_name = Path(pdf_path).name
    identifier = Path(pdf_path).stem

    mets_record = parse_mets(pdf_file_name)
    pages = get_pdf_pages_of_book(pdf_file_name)
    images = extract_images(pdf_path)

    transcribe_dir = Path(f"../data/transcriptions/{identifier}/")
    transcribes = [p for p in transcribe_dir.iterdir() if p.name.startswith('transcribe')]
    transcribes = sorted(transcribes)

    bboxes = []
    for transcribe in transcribes:
        bboxes += get_bounding_boxes_from_transcription(str(transcribe))
    for page_nr, (_, image), rec in zip(pages, images, bboxes):
        if len(rec["lines"]) > 0:

            render_set = {
                "image_name": page_nr,
                "image_width": rec["image_size"][0],
                "image_height": rec["image_size"][1],
                "writing_mode": rec["writing_mode"],
                "lines": rec["lines"],
                "text": "\n".join([l['text'] for l in rec["lines"]])
            }

            serialized_page = serialize_page(
                render_set,
                mets_record['source_url'],
                mets_record['language']
            )

            output_path = Path(f"../data/xml_output/{identifier}_{page_nr}")
            output_path = output_path.with_suffix(".xml")
            with open(output_path, "w") as fout:
                fout.write(serialized_page)
        else:
            print(f"no text found for {identifier} on page {page_nr} of {pages}")
if __name__ == '__main__':
    main()
