from PyPDF2 import PdfFileMerger


def main():
    f = open("../data/data.json", "r+")
    data = json.load(f)
    f.close()
    
    for book in data:
        
        pdfs = data[book]["pdfs"]
        merger = PdfFileMerger()

        for pdf in pdfs:
            merger.append("../data/pdf_download/" pdf)

        merger.write("../data/split_pdf/" +book + ".pdf")
        merger.close

if __name__ == '__main__':
    main()

