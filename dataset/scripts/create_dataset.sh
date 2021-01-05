book="de_robe"

declare -a pn_list
pn_list=$(python3 book_from_json.py --book $book)
#pn_list=$(python3 process_csv.py --book $book --csv ../data/books.csv)


arr=($pn_list)

id=${arr[0]}
num_transcribes=${arr[1]}
pn_list=${arr[@]:2}

echo $id
echo $num_transcribes
echo $pn_list

mkdir ../data/split_img/$book/

python3 split_pdfs.py \
    --pdf_path ../data/split_pdf/$book.pdf \
    --pagenr_list "$pn_list" \
    --out_dir ../data/split_img/$book/

arr=($pn_list)


#prepare multiple transcribe inputs for html2hocr.p
transcribes=""
for i in `seq 1 $num_transcribes`
do
    transcribes+=" -t ../data/transcriptions/$book/"
    if [ $i == 1 ]
    then
        transcribes+="transcribe.html"
    else
        transcribes+="transcribe$i.html"
    fi
done

#prepare multiple image inputs for html2hocr.p
images=""
for i in "${arr[@]}"
do
    images+=" -i ../data/split_img/$book/$i.png"    
done

    
python3 html2hocr.py \
    $transcribes \
    $images \
    -o ../data/transcriptions/$book/$book.hocr \
    -u $id
    
mkdir ../data/split_snippets/$book/
    
python3 process_hocr.py \
    --hocr_path ../data/transcriptions/$book/$book.hocr \
    --pagenr_list "$pn_list" \
    --in_dir ../data/split_img/$book/ \
    --out_dir ../data/split_snippets/$book/
