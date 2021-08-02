import sys
sys.path.append("../utils/")
from pathlib import Path
import click

from pdfs import extract_images
from shutil import copy



@click.command()
@click.option('--pdf_path')
def main(pdf_path):
    
    images = extract_images(pdf_path)
    for image_path, image in images:
        image.save(Path(image_path).name)

if __name__ == '__main__':
    main()
# main('../data/pdf_renamed/1VUJAAAAQAAJ.pdf')