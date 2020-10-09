import numpy as np
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import glob
import os
from lxml import etree
from PIL import Image
import base64
import io

from html.parser import HTMLParser
import click



'''=================================================================================


1. Iterate over PDFS/XML and collect a list L with {page_nr, crop_points, text}

2. Iterate over L and crop+save images + text


TODO:
    - delete \t and \n in textoutput?
    - change the name of the outputted datas


=================================================================================='''

# load pic
#iterate trhough

@click.command()
@click.option('--hocr_path')
@click.option('--pagenr_list')
@click.option('--in_dir')
@click.option('--out_dir')
def main(hocr_path, pagenr_list, in_dir, out_dir):
    
    
    pn_list = pagenr_list[1:-1].split(",")
    
    
    L = []
    #pn_list = ["1047.png", "1344.png", "1824.png"]

    f = open(hocr_path)
    hocr = f.read()
    
    
    
    tree = etree.fromstring(hocr)
    images = tree.xpath('//div')
    count = 0
    
    for i in range(len(images)):
        for j in range(len(images[i])):
            if len(dict(images[i][j].attrib).keys()) > 0:
                bbox = list(map(int, ((images[i][j].attrib["title"].split("]"))[0].split("[")[-1]).split(",")))
                l = [in_dir+pn_list[i]+".png", bbox, "".join(images[i][j].itertext())]
                L.append(l)

    #=================================================================================
    

    print("start cropping")
    count = 0
    for l in L:

        #open respective image
        img = Image.open(l[0])
        
        #get x1, y1, x2, y2, image path and text from l
        coords = l[1]
        
        #crop image
        try:
            #crop + save image
            cropped_img = img.crop(coords)
            cropped_img.save("{}{}.png".format(out_dir, count))
            
            #save text
            f = open("{}{}txt".format(out_dir, count), "w")
            txt = l[2].replace("\t", "").replace("\n", "")
            f.write(txt)
            f.close()
            
            count += 1
            
        except:
            print("problem", l)
            
        
        
        
if __name__ == "__main__":
    main()
