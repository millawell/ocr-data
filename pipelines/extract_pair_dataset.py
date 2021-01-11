import sys
sys.path.append("../utils/")
from pathlib import Path
import click

from sheet import get_pdf_pages_of_book
from transcriptions import get_bounding_boxes_from_transcription
from pdfs import extract_images

from lxml import etree

def parse_bbox(title_str):
    return list(
        map(
            int,
            title_str \
                .split("[")[1]   \
                .split("]")[0]   \
                .split(",")
        )
    )

def extract_page(page_el, image):
    lines = page_el.xpath(".//span[@class='ocr_line']")

    for line in lines:

        coords = parse_bbox(line.attrib['title'])

        yield (
            line.text,
            image.crop(coords)
        )

@click.command()
@click.option('--pdf_path')
def main(pdf_path):

    pdf_file_name = Path(pdf_path).name
    images = extract_images(pdf_path)
    xml_file_name = Path(f"../data/xml_output/{pdf_file_name}")
    xml_file_name = xml_file_name.with_suffix(".hocr")

    with open(xml_file_name) as fin:
        tree = etree.fromstring(fin.read())

    image_pages = tree.xpath('//div')
    
    out_dir = Path(f"../data/pair_output/")
    out_dir.mkdir(exist_ok=True)

    file_id = 0
    for iimage, page_el in enumerate(image_pages):
        image = images[iimage][1]
        for text, crop in extract_page(page_el, image):

            txt_filename = out_dir / f"{Path(pdf_path).stem}_{file_id:08d}.txt"
            img_filename = out_dir / f"{Path(pdf_path).stem}_{file_id:08d}.png"

            with open(txt_filename, 'w') as fout:
                fout.write(text)

            crop.save(img_filename)
            file_id += 1

if __name__ == '__main__':
    main()
# main('../data/pdf_renamed/1VUJAAAAQAAJ.pdf')