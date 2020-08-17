import os
import shutil
import click
import subprocess



@click.command()
@click.option('--pdf_path')
@click.option('--pagenr_list')
def main(pdf_path, pagenr_list):
    
    
    
    print(pdf_path)
    
    
    pn_list = map(int,pagenr_list[1:-1].split(","))
    
    for pagenr in pn_list:
        
        print(pagenr)
        
        #get image_root
        #get pagenr
        
        image_root = str(pagenr)
    
        command = "pdfimages -png -f {} -l {} {} {}".format(pagenr, pagenr ,pdf_path, image_root).split(" ")
        subprocess.call(command)
    
    
        #rename single images
        
        
        #Delete google watermarks
        command = 'find -name "*.png" -type f -size -10k -delete'
        subprocess.call(command, shell=True)
    
    
    
    return



    
    
    
    
    
    '''
    
    example:
    
    python3 split_pdfs.py --pdf_path anne.pdf --pagenr_list [1,2,3]
    
    
    '''


        
if __name__ == "__main__":
    main()
