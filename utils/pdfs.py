import subprocess
from pathlib import Path
from mets import get_pdf_pages_of_book
import tempfile
from PIL import Image, ImageOps    
import numpy as np

def sort_images_as_in_sheet(images, true_order):
    result = []

    images_lookup = {int(img[0].stem.split("-")[0]):img for img in images}

    for c in true_order:
        result.append(images_lookup[c])

    return result

def ensure_not_inverted(img):
    if np.median(np.array(img)) == 0:
        img = ImageOps.invert(img)
    return img

def extract_images(pdf_path):
    pdf_file_name = Path(pdf_path).name
    identifier = Path(pdf_path).stem
    
    pages = get_pdf_pages_of_book(pdf_file_name)
    images = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        for pagenr in pages:
        
            command = f"pdfimages -png -f {pagenr} -l {pagenr} {pdf_path} {tmp_dir}/{pagenr}-{identifier}"
            subprocess.call(command, shell=True)

            #Delete google watermarks
            command = f'find {tmp_dir} -name "*.png" -type f -size -10k -delete'
            subprocess.call(command, shell=True)

            tmp_images = []
            for fn in list(Path(tmp_dir).iterdir()):
                if fn.stem.startswith(str(pagenr)):
                    tmp_images.append((fn, Image.open(fn)))

            if len(tmp_images) == 3:
                for tmp_image in tmp_images:
                    if tmp_image[1].mode != '1':
                        tmp_image[0].unlink()
        
        for img in Path(tmp_dir).iterdir():  
            # deskew images
            command = f"convert {img} -deskew 40% -set option:deskew:auto-crop false {img}"
            subprocess.call(command, shell=True)
            images.append((
                img, 
                ensure_not_inverted(Image.open(img))
            ))
    
    images = sort_images_as_in_sheet(images, pages)

    return images

# imgs = extract_images('../data/pdf_renamed/3pVMAAAAcAAJ.pdf')
