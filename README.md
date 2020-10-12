# ocr-data

In order to create the dataset, the two following python programs have to be executed:

-split_pdfs.py
-process_hocr.py 


The split_pdfs.py script takes a PDF file as input and outputs single predefined pages of the PDF as PNG images. In addition the script deletes automaticall generated watermark images.
Input:
    --pdf_path      : path to the PDF file
    --pagenr_list   : list of pages to extract
    --out_dir       : path to the directory to save PNGs of single pages

Example usage:
python3 split_pdfs.py \
    --pdf_path split/de_wood.pdf \
    --pagenr_list [24,51,63] \
    --out_dir ./transcriptions/de_wood/test2/


The process_hocr.py uses the precomputed PNG images and an hocr file to create small image/text snippets containing only a single line.
Input:
    --hocr_path     : path to the HOCR file
    --pagenr_list   : list of pages to process (image names of the processing PNGs)
    --in_dir        : path to directory of saved PNGs of single pages
    --out_dir       : path to directory to save pairs of line-image snippet and line-text snippet


Example usage:
python3 process_hocr.py \
    --hocr_path ./transcriptions/de_wood/de_wood.hocr \
    --pagenr_list [24,51,63] \
    --in_dir ./transcriptions/de_wood/test2/ \
    --out_dir ./transcriptions/de_wood/test3/

    
    
    
Python libary requirements: 
import click
import subprocess
from PIL import Image
from lxml import etree
