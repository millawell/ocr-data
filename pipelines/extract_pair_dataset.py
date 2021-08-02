import sys
sys.path.append("../utils/")
from pathlib import Path
from mets import parse_mets
import click

from transcriptions import get_bounding_boxes_from_transcription
from pdfs import extract_images

from lxml import etree

pc={'pc':'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15'}

def points_to_bbox(points):
    
    #'0,0 2501,0 2501,4042 2501,4042'
    points = points.split(" ")
    
    top = int(points[0].split(",")[0])
    right = int(points[1].split(",")[1])
    left = int(points[0].split(",")[1])
    bottom = int(points[2].split(",")[0])
    return [left, top, right, bottom]

def extract_page(page_el, image):
    lines = page_el.xpath(".//pc:TextLine", namespaces=pc)

    image_size = page_el.find(
        ".//pc:PrintSpace/pc:Coords",
        namespaces=pc
    ).attrib['points']

    page_image_size = points_to_bbox(image_size)[2:]
    
    image = image.resize(page_image_size)
    
    for line in lines:
        
        coords = line.find( 
            './/pc:Coords',
            namespaces=pc
        ).attrib['points']
        coords = points_to_bbox(coords)

        text = line.find(
            './/pc:Unicode',
            namespaces=pc
        ).text
        # import matplotlib.pyplot as plt
        # import matplotlib.patches as patches
        # from PIL import Image
        # import numpy as np
        # fimage = np.array(Image.open("/Users/davidlassner/code/ocr-data/data/transcriptions/zviTtwEACAAJ/1047.png"))
        # _, (ax0, ax1) = plt.subplots(ncols=2)
        # ax0.imshow(image, cmap='gray')
        # rect = patches.Rectangle((coords[0], coords[1]), coords[2]-coords[0], coords[3]-coords[1], linewidth=1, edgecolor='r')
        # ax0.add_patch(rect)
        # ax1.imshow(fimage, cmap='gray')
        # rect = patches.Rectangle((coords[0], coords[1]), coords[2]-coords[0], coords[3]-coords[1], linewidth=1, edgecolor='r')
        # ax1.add_patch(rect)
        # plt.show()
        # import pdb; pdb.set_trace()
        ###
        yield (
            text.strip(),
            image.crop(coords)
        )

@click.command()
@click.option('--pdf_path')
def main(pdf_path):
    root = Path("..")
    pdf_file_name = Path(pdf_path).name
    mets_record = parse_mets(pdf_file_name)
    xml_files = mets_record["xml_files"]
    rerouted_files = []
    for xml_file in xml_files:
        rerouted_files.append(
            root / Path(xml_file)
        )
    xml_files = rerouted_files

    images = extract_images(pdf_path)
    # import pdb; pdb.set_trace()
    file_id = 0
    for xml_file, image in zip(xml_files, images):
        if xml_file.exists():
            with open(xml_file) as fin:
                tree = etree.fromstring(fin.read().encode('utf-8'))
            image_pages = tree.xpath('//pc:Page', namespaces=pc)

            out_dir = Path(f"../data/pair_output/")
            out_dir.mkdir(exist_ok=True)
            
            for iimage, page_el in enumerate(image_pages):
                # image = images[iimage][1]
                # import pdb; pdb.set_trace()
                for text, crop in extract_page(page_el, image[1]):

                    txt_filename = out_dir / f"{Path(pdf_path).stem}_{file_id:08d}.txt"
                    img_filename = out_dir / f"{Path(pdf_path).stem}_{file_id:08d}.png"

                    with open(txt_filename, 'w') as fout:
                        fout.write(text)

                    crop.save(img_filename)
                    file_id += 1

if __name__ == '__main__':
    main()
# main('../data/pdf_renamed/1VUJAAAAQAAJ.pdf')