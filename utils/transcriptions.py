from lxml import html, etree
import base64
from PIL import Image
from io import BytesIO
from kraken.rpred import ocr_record

def get_images_from_transcription(path):
    doc = html.parse(path)
    etree.strip_tags(doc, etree.Comment)
    img_divs = doc.findall(".//div[@class='img_container']")
    
    images = []
    for img_div in img_divs:
        data = img_div.find('./img').attrib['src']
        data = data[len('data:image/png;base64,'):]
        im = Image.open(BytesIO(base64.b64decode(data)))
        images.append(im)

    return images


def get_bounding_boxes_from_transcription(path):
    
    doc = html.parse(path)
    etree.strip_tags(doc, etree.Comment)
    td = doc.find(".//meta[@itemprop='text_direction']")
    
    if td is None:
        td = 'horizontal-lr'
    else:
        td = td.attrib['content']
    records = []

    for isection, section in enumerate(doc.xpath('//section')):
        
        records.append({
            "writing_mode":td,
            "lines": []
        })
        for line in section.iter('li'):
            if line.get('contenteditable') and (not u''.join(line.itertext()).isspace() and u''.join(line.itertext())):
                left, upper, right, lower = [int(x) for x in line.get('data-bbox').split(',')]
                
                # add some margin on the edges
                width = right-left
                height = lower-upper
                left = int(left - width*.025)
                right = int(right + width*.025)
                upper = int(upper - height*.025)
                lower = int(lower + height*.05)

                text = u''.join(line.itertext()).strip()
                rec = ocr_record(
                    text, [[left,upper,right,lower]], [1.0]*len(text)
                )
                records[-1]["lines"].append({
                    'text': rec.prediction,
                    'bbox': rec.cuts
                })
    
    return records

# recs = get_bounding_boxes_from_transcription('../data/transcriptions/2jMfAAAAMAAJ/transcribe.html')