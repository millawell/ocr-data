#import os
#import shutil
import click
import subprocess



@click.command()
@click.option('--pdf_path')
@click.option('--pagenr_list')
@click.option('--out_dir')
def main(pdf_path, pagenr_list, out_dir):
    
    
    
    print(pdf_path)
    
    
    #pn_list = map(int,pagenr_list[1:-1].split(","))
    pn_list = list(map(int,pagenr_list.split(" ")))
    print("split_pdfs", pn_list)
    
    for pagenr in pn_list:
        
        print(pagenr)
        
        #get image_root
        #get pagenr
        
        image_root = out_dir + str(pagenr)
    
        command = "pdfimages -png -f {} -l {} {} {}".format(pagenr, pagenr ,pdf_path, image_root).split(" ")
        subprocess.call(command)
    
    
        #rename single images
        
        
        #Delete google watermarks
        command = 'find {} -name "*.png" -type f -size -10k -delete'.format(out_dir)
        subprocess.call(command, shell=True)
        
        #Delete google watermarks
        command = 'mv {}{}-000.png {}{}.png'.format(out_dir, pagenr,out_dir, pagenr)
        print(command)
        subprocess.call(command, shell=True)
    
    
    
    return



    
    
    
    
    
    '''
    
    example:
    
    python3 split_pdfs.py --pdf_path anne.pdf --pagenr_list [1,2,3]
    
    
    '''


        
if __name__ == "__main__":
    main()
