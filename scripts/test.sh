    
#transform html to hocr
python3 html2hocr.py \
    -t ./transcriptions/de_wood/transcribe.html \
    -i ./transcriptions/de_wood/068.png \
    -i ./transcriptions/de_wood/149.png \
    -i ./transcriptions/de_wood/185.png \
    -o ./transcriptions/de_wood/de_wood.hocr \
    -u ./split/de_wood.pdf 

#get single pages from pdf
python3 split_pdfs.py \
    --pdf_path split/de_wood.pdf \
    --pagenr_list [24,51,63] \
    --out_dir ./transcriptions/de_wood/test2/

#git single lines from single pages
python3 process_hocr.py \
    --hocr_path ./transcriptions/de_wood/de_wood.hocr \
    --pagenr_list [24,51,63] \
    --in_dir ./transcriptions/de_wood/test2/ \
    --out_dir ./transcriptions/de_wood/test3/

