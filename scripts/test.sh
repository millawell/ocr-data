

book="de_anna"
pn_list=$(python3 process_csv.py --book $book)
echo $pn_list

mkdir ./trans_test/$book/

python3 split_pdfs.py \
    --pdf_path split/$book.pdf \
    --pagenr_list "$pn_list" \
    --out_dir ./trans_test/$book/

arr=($pn_list)
    
python3 html2hocr.py \
    -t ./transcriptions/$book/transcribe.html \
    -i ./trans_test/$book/${arr[0]}.png \
    -i ./trans_test/$book/${arr[1]}.png \
    -i ./trans_test/$book/${arr[2]}.png \
    -o ./trans_test/$book/$book.hocr \
    -u ./split/$book.pdf 
    
mkdir ./trans_test/$book/data/
    
python3 process_hocr.py \
    --hocr_path ./trans_test/$book/$book.hocr \
    --pagenr_list "$pn_list" \
    --in_dir ./trans_test/$book/ \
    --out_dir ./trans_test/$book/data/
