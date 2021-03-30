from pathlib import Path
import pandas as pd
from lxml import etree
from urllib.parse import urlparse

def el_list_to_id_indexed_dict(el_list):
    result = {}
    for el in el_list:
        result[el.attrib['ID']] = el
    return result


def parse_mets(pdf_name):

    path_to_mets = Path("../data/mets/") / pdf_name
    path_to_mets = path_to_mets.with_suffix(".mets.xml")
    raw_file_contents = open(path_to_mets).read().encode('utf-8')
    tree = etree.fromstring(raw_file_contents)

    namespaces = {
        "mets":"http://www.loc.gov/METS/",
        "dc": "http://purl.org/dc/elements/1.1/"

    }
    pdf_files = tree.xpath(
        "//mets:file[@MIMETYPE='application/pdf']",
        namespaces=namespaces
    )
    pdf_files = el_list_to_id_indexed_dict(pdf_files)

    xml_files = tree.xpath(
        "//mets:file[@MIMETYPE='text/xml']",
        namespaces=namespaces
    )
    xml_files = el_list_to_id_indexed_dict(xml_files)

    file_map = tree.xpath(
        "//mets:structMap/mets:div",
        namespaces=namespaces
    )

    language = tree.xpath(
        "//dc:language",
        namespaces=namespaces
    )
    assert len(language) == 1, 'no unique language definition found.'
    language = language[0].attrib['content']
    
    record = {
        "xml_files":[],
        "source_urls": [],
        "page_numbers":[],
        "identifier":None,
        "language": language
    }
    for div in file_map:
        for fptr in div.xpath("./mets:fptr", namespaces=namespaces):
            query_id = fptr.attrib["FILEID"]
            record['identifier'] = query_id.split("_")[1]
            if query_id.startswith("gt_"):
                xml_file = xml_files[query_id]
                flocat = xml_file.find(".//mets:FLocat", namespaces=namespaces)
                record['xml_files'].append(
                    flocat.attrib['{http://www.w3.org/1999/xlink}href']
                )

            elif query_id.startswith("pdf_"):
                pdf_file = pdf_files[query_id]
                flocat = pdf_file.find(".//mets:FLocat", namespaces=namespaces)
                url = urlparse(flocat.attrib['{http://www.w3.org/1999/xlink}href'])
                page_nr = url.fragment.split("page=")[1]
                record['page_numbers'].append(page_nr)
                record['source_url'] = url.geturl().split("#page=~")[0]
            else:
                raise ValueError("query id type unknown.")

    return record


def get_pdf_pages_of_book(pdf_name):
    mets = parse_mets(pdf_name)
    return list(map(int, mets['page_numbers']))

