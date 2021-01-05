import click
import tensorflow
import ntpath
from lxml import html, etree
from PIL import Image
from jinja2 import Environment, FileSystemLoader
from kraken.rpred import ocr_record
from kraken.serialization import _rescale

def serialize(predictions, urlpdf):
    pages = []
    for pred in predictions:
        image_name = pred["image_name"]
        image_size = pred["image_size"]
        writing_mode = pred["writing_mode"]
        lines = pred["lines"]

        page = {'lines': [], 'size': image_size, 'name': image_name, 'writing_mode': writing_mode, 'scripts': None}  # type: dict
        seg_idx = 0
        char_idx = 0
        for idx, record in enumerate(lines):
            line = {'index': idx,
                    'bbox': record.cuts,
                    'text': record.prediction
                    }
            page['lines'].append(line)
        pages.append(page)

    env = Environment(
        loader=FileSystemLoader('templates'),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True
    )
    env.tests['whitespace'] = str.isspace
    env.filters['rescale'] = _rescale
    tmpl = env.get_template("hocr_lines.xml")
    return tmpl.render(pages=pages, urlpdf=urlpdf)

"""
Example usage:
python html2hocr.py \
    -t ../in_data/de_gros/transcribe.html \
    -t ../in_data/de_gros/transcribe2.html \
    -t ../in_data/de_gros/transcribe3.html \
    -i ../in_data/de_gros/060.png \
    -i ../in_data/de_gros/285.png \
    -i ../in_data/de_gros/656.png \
    -i ../in_data/de_gros/372.png \
    -i ../in_data/de_gros/228.png \
    -i ../in_data/de_gros/129.png \
    -i ../in_data/de_gros/066.png \
    -i ../in_data/de_gros/372.png \
    -i ../in_data/de_gros/228.png \
    -i ../in_data/de_gros/129.png \
    -i ../in_data/de_gros/066.png \
    -o de_gros.hocr \
    -u de_gros.html 
"""

@click.command()
@click.option(
    "-t",
    '--transcriptions',
    multiple=True,
    type=click.File(mode='rb', lazy=True)
)
@click.option(
    "-i",
    '--images',
    multiple=True,
    type=str
)
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path()
)
@click.option(
    "-u",
    "--urlpdf",
    required=True,
    type=click.Path()
)
def main(transcriptions, images, output, urlpdf):
    images = [it for it in images]
    for fp in transcriptions:
        doc = html.parse(fp)
        etree.strip_tags(doc, etree.Comment)
        td = doc.find(".//meta[@itemprop='text_direction']")
        
        if td is None:
            td = 'horizontal-lr'
        else:
            td = td.attrib['content']
        records = []

        for isection, section in enumerate(doc.xpath('//section')):
            
            img = images.pop(0)
            section_id = ntpath.basename(img).split(".")[0]
            img = Image.open(img)

            records.append({
                "image_name":section_id,
                "image_size":img.size,
                "writing_mode":td,
                "lines": []
            })
            for line in section.iter('li'):
                if line.get('contenteditable') and (not u''.join(line.itertext()).isspace() and u''.join(line.itertext())):
                    bbox = [int(x) for x in line.get('data-bbox').split(',')]
                
                    text = u''.join(line.itertext()).strip()
                    rec = ocr_record(
                        # prediction: str, cuts, confidences: List[float]
                        text, [bbox], [1.0]*len(text)
                    )
                    records[-1]["lines"].append(rec)

    serialized = serialize(
        records,
        urlpdf
    )
    with open(output, "w") as fout:
        fout.write(serialized)

if __name__ == '__main__':
    main()
